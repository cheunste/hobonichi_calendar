import hobonichi_calendar as hobo
import os
from PIL import Image, ImageOps


class FinalImage():
    final_image_name = "Final_print.jpg"
    path = ""
    width_ptr = 0
    height_ptr = 0

    def __init__(self, output_path, size_in_pixel):
        self.path = f"{output_path}/{self.final_image_name}"
        hobo.Create_Blank_Image(self.path, size_in_pixel)

    def get_path(self):
        return self.path

    def paste_thumbnail(self, thumbnail_path):
        return
