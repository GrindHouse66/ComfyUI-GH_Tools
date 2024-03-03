import math

class GHImg_Sizer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Width": ("INT",{
                    "default": 1024,
                    "step":1,
                    "display": "number"
                }),                
                "Aspect_Ratio_Width": ("INT",{
                    "default": 1,
                    "step":1,
                    "display": "number"
                }),
                "Aspect_Ratio_Height": ("INT",{
                    "default": 1,
                    "step":1,
                    "display": "number"
                })
            }
        }

    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("Width", "Height")

    FUNCTION = "run"

    CATEGORY = "GH_Tools"

    def run(self, Width, Aspect_Ratio_Width, Aspect_Ratio_Height):
        # Taking the image base width and an aspect ratio, calculate and appropriate heitgh value and return it
              
        # Calculate the aspect ratio decimal
        aspect_ratio_decimal = Aspect_Ratio_Width / Aspect_Ratio_Height
        
        # Calculate width and height
        #width = math.sqrt(pixels * aspect_ratio_decimal)
        Height = Width / aspect_ratio_decimal
        
        # Return the width and height as a tuple of integers
        return (int(round(Width)), int(round(Height)))
    
NODE_CLASS_MAPPINGS = {
    "GHImg_Sizer": GHImg_Sizer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GHImg_Sizer": "GH Tools Image Sizer"
}