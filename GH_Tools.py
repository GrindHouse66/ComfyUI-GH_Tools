import math

class GHImg_Sizer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "Image_Width": ("INT",{
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
                "Width": ("WIDTH",),                
                "Height": ("HEIGHT",),
                "Scale": ("FLOAT",{
                    "default": 2,
                    "min": 0.00,
                    "max": 10.00,
                    "step":0.01,
                    "display": "number"
                })
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
    
NODE_CLASS_MAPPINGS = {
    "GHImg_Sizer": GHImg_Sizer,
    "GHSimple_Scale": GHSimple_Scale
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GHImg_Sizer": "GH Tools Image Sizer",
    "GHSimple_Scale": "GH Tools Simple Scale"
}