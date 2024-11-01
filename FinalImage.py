import hobonichi_calendar as hobo
import os
from PIL import Image, ImageOps


class FinalImage():
    final_image_name = "Final_print.jpg"
    path = ""
    # Pointers. To keep track of where the next thumbnail should be placed
    width_ptr = 0
    height_ptr = 0

    # this is an indication of the tallest thumbnail that's currently in the final image
    # Used to address to a new row if the width of the final image is exceeded
    tallest_image_height = 0

    def __init__(self, name, output_path, size_in_pixel):
        self.final_image_name = name
        self.path = f"{output_path}{self.final_image_name}"
        hobo.Create_Blank_Image(self.path, size_in_pixel)

    def get_all_thumbnails(self, output_path, temp_name):
        t = []
        for root, dir, files in os.walk(f"{output_path}", topdown=True):
            exclude = set([f'{temp_name}', 'New folder',
                           'Windows', 'Desktop', f'{temp_name}'])
            dir[:] = [d for d in dir if d not in exclude]
            for f in files:
                file_path = f"{output_path}/{f}"
                if file_path.__contains__(".DS_Store") or file_path.__contains__(self.final_image_name):
                    pass
                else:
                    t.append(file_path)
        return t

    def get_path(self):
        return self.path

    def paste_thumbnails(self, thumbnail_list):
        for thumbnail_path in thumbnail_list:
            self.paste_thumbnail(thumbnail_path)

    def paste_thumbnail(self, thumbnail_path):
        t = Image.open(thumbnail_path)

        (tw, th) = t.size

        if self.is_over_final_image_width(tw):
            self.__increment_height_ptr()
            self.width_ptr = 0
            pass
        if self.is_over_final_image_height(th):
            raise HeightOutOfBoundException("Image Height Out of Bound")
            return

        self.__paste(t)
        t.close

    def is_over_final_image_width(self, thumbnail_width):
        print(f"Warning: {thumbnail_width} is greater than the image width. Pasting image cannot take place")
        return self.width_ptr + thumbnail_width > Image.open(self.path).width

    def is_over_final_image_height(self, thumbnail_height):
        print(f"Warning: {thumbnail_height} is greater than the image height. New {self.final_image_name} need to be be created ")
        return self.height_ptr + thumbnail_height > Image.open(self.path).height

    def get_width_ptr(self):
        return self.width_ptr

    def get_height_ptr(self):
        return self.height_ptr

    def __paste(self, thumbnail_image):
        f = Image.open(f"{self.path}")
        f.paste(thumbnail_image, (self.width_ptr, self.height_ptr))
        f.save(self.path)
        self.width_ptr = self.width_ptr+thumbnail_image.width
        self.tallest_image_height = self.height_ptr+thumbnail_image.height
        f.close

    def __increment_height_ptr(self):
        self.height_ptr = self.tallest_image_height


class HeightOutOfBoundException(Exception):
    pass
