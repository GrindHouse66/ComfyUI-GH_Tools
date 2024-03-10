import math
import os
import sys
import json
import random
from pathlib import Path
from PIL import Image, ImageOps, ImageSequence
from PIL.PngImagePlugin import PngInfo
import numpy as np
from comfy.cli_args import args

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "comfy"))

import folder_paths

#Set paths for future use
BASEDIR = Path.cwd()                                        #ComfyUI base folder
MODELSDIR = BASEDIR.joinpath("ComfyUI", "models")           #ComfyUI models folder
CHKPNTSDIR = MODELSDIR.joinpath("checkpoints")              #ComfyUI checkpoints folder
LORASDIR = MODELSDIR.joinpath("loras")                      #ComfyUI loras folder
VAEDIR = MODELSDIR.joinpath("vae")                          #ComfyUI vae folder

MAX_RESOLUTION=8192
VWR_MODES = ["Bypass", "Preview", "Save"]

class GHImg_Sizer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Image_Width": ("INT",{"default": 1024, "step":8, "min": 8, "max": MAX_RESOLUTION, "display": "number"}),                
                "Aspect_Ratio_Width": ("INT",{"default": 1, "step":1, "display": "number"}),
                "Aspect_Ratio_Height": ("INT",{"default": 1, "step":1, "display": "number"})
            }
        }

    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("Width", "Height")

    FUNCTION = "calcheight"

    CATEGORY = "GH_Tools"

    def calcheight(self, Image_Width, Aspect_Ratio_Width, Aspect_Ratio_Height):
        # Taking the image base width and an aspect ratio, calculate and appropriate height value and return it
              
        # Calculate the aspect ratio decimal
        aspect_ratio_decimal = Aspect_Ratio_Width / Aspect_Ratio_Height
        
        # Calculate height from Width and aspect ratio
        # Ensure Width is a multiple of 8 before dividing by Aspect Ratio
        Height = (((Image_Width + 7) // 8) * 8) / aspect_ratio_decimal
        
        # Return the width and height as a tuple of integers
        # Ensure Height is a multiple of 8 before returning
        return (int(round(((Image_Width + 7) // 8) * 8)), int(round((Height + 7) // 8) * 8))
    
class GHSimple_Scale:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Width": ("INT", {"forceInput": True}),                
                "Height": ("INT", {"forceInput": True}),
                "Scale": ("FLOAT",{"default": 2.00, "min": 0.01, "max": 10.00, "step":0.01, "display": "number"})
            }
        }

    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("Width", "Height")

    FUNCTION = "rescale"

    CATEGORY = "GH_Tools"

    def rescale(self, Width, Height, Scale):
        # Accepts Width and Height from a node connection, and scales based on user input
              
        # Calculate the aspect ratio decimal
        S_Width = Width*Scale
        S_Height = Height*Scale
        
        
        # Return the width and height as a tuple of integers
        # Ensure Height is a multiple of 8 before returning
        return (int(round(((S_Width + 7) // 8) * 8)), int(round((S_Height + 7) // 8) * 8))


# GHImg_Vwr is based on the original SaveImage and PreviewImage Nodes
class GHImg_Vwr:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"modes": ("[Bypass, Preview, Save]", {"default": "Bypass"}), 
                     "images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "ComfyUI"})},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
                }

    RETURN_TYPES = ()
    FUNCTION = "Image_Viewer"

    OUTPUT_NODE = True

    CATEGORY = "GH_Tools"

    def Image_Viewer(self, images, modes, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        modes = modes
        if modes == "Bypass":
            print("Mode - Bypass")
            return (images)
        elif modes == "Preview":
            print("Mode - Preview")
            self.save_images(images, filename_prefix, prompt, extra_pnginfo)
        elif modes == "Save":
            print("Mode - Save")
            self.save_images(images, filename_prefix, prompt, extra_pnginfo)
        return {} 

    def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "images": results } } 
    
    def preview_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        self.output_dir = folder_paths.get_temp_directory()
        self.type = "temp"
        self.prefix_append = "_temp_" + ''.join(random.choice("abcdefghijklmnopqrstupvxyz") for x in range(5))
        self.compress_level = 1

        @classmethod
        def INPUT_TYPES(s):
            return {"ui": {"images": ("IMAGE", ), }, }

    
NODE_CLASS_MAPPINGS = {
    "GHImg_Sizer": GHImg_Sizer,
    "GHSimple_Scale": GHSimple_Scale,
    "GHImg_Vwr": GHImg_Vwr
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GHImg_Sizer": "GH Tools Image Sizer",
    "GHSimple_Scale": "GH Tools Simple Scale",
    "GHImg_Vwr": "GH Tools Image Viewer"
}
