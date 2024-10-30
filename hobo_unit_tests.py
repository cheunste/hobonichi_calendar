import unittest
import hobonichi_calendar as hobo
import FinalImage as fi
import os
from PIL import Image, ImageOps


class Test_Hobonichi_Calendar(unittest.TestCase):

    # Both test_width and test_height are in inches
    test_width = 8.5
    test_height = 8.5
    test_thumbnail = "./ForHobonichi/test.png"

    def test_calculate_papersize(self):
        self.assertTrue(hobo.Get_PaperSize() == (8.5, 11))

    def test_get_cousin_calendar_size(self):
        self.assertTrue(hobo.Get_Cousin_Calendar_Size() == (3.3, 2.6))

    def test_get_file_type(self):
        self.assertTrue(hobo.Get_Supported_File_Types() == [("JPEG (*.jpg)", "*.jpg", "*.heic","*.HEIC"),("All files (*.*)", "*.*")])

    def test_in_cm_convert(self):
        r = hobo.Inches_To_Cm(8.5)
        self.assertTrue(r == 21.59)

    def test_pixel_to_cm(self):
        self.assertTrue(hobo.Pixel_To_Centimeter(800) == 2032)
        self.assertTrue(hobo.Pixel_To_Centimeter(3000,200) == 38)

    def test_cm_to_pixel(self):
        self.assertTrue(hobo.Centimeter_To_Pixel(1, 200) == 79)

    def test_create_new_image(self):
        p = "./test.jpg"
        hobo.Create_Blank_Image(p, (300, 300))
        r = os.path.exists(p)
        self.assertTrue(r)

    def test_rescale(self):
        hobo.shrink_image("./furret.JPG", "./furrent_rescale.jpg", (150, 150))
        self.assertTrue("./furret_rescale.jpg")

        print(hobo.Length_To_Pixel(hobo.Get_Cousin_Calendar_Size()))
        hobo.shrink_image("./furret.JPG", "./furrent_rescale2.jpg",
                          hobo.Length_To_Pixel(hobo.Get_Cousin_Calendar_Size()))
        self.assertTrue("./furret_rescale2.jpg")

    def test_rescale_heic(self):
        hobo.shrink_image("./roundboys.HEIC", "./roundboys_rescale.jpg", (150, 150))
        self.assertTrue("./roundboys_rescale.jpg")

    def test_crop(self):
        size = (490, 140, 930, 720)
        hobo.crop("./furret.JPG", "./furrent_crop.jpg", size)
        self.assertTrue("./furret_crop.jpg")

    def test_landscape_or_portrait(self):
        self.assertTrue(hobo.is_landscape("./surfing_pikachu.JPG"))
        self.assertFalse(hobo.is_portrait("./surfing_pikachu.JPG"))

    def test_landscape_or_portrait_heic_file(self):
        self.assertTrue(hobo.is_landscape("./roundboys.HEIC"))
        self.assertFalse(hobo.is_portrait("./roundboys.HEIC"))

    def test_put_to_final_image(self):
        p = "./"
        size_in_pixel = hobo.Length_To_Pixel(
            (self.test_width, self.test_height), is_inches=True)
        fi.FinalImage("Final_print.jpg", p, size_in_pixel)

        r = os.path.exists(p)
        self.assertTrue(r)

        i = Image.open(f"./Final_print.jpg")
        (w, h) = i.size
        (nw, nh) = hobo.Length_To_Pixel(
            (self.test_width, self.test_height), is_inches=True)
        self.assertTrue(w == nw)
        self.assertTrue(h == nh)

    def test_paste_thumbnail_to_final_image(self):

        size_in_pixel = hobo.Length_To_Pixel(
            (self.test_width, self.test_height), is_inches=True)

        f = fi.FinalImage("test.jpg", "./", size_in_pixel)
        i = f.get_path()
        s = Image.open(self.test_thumbnail)
        (w, h) = s.size
        f.paste_thumbnail(self.test_thumbnail)

        expected_w = s.width
        expected_h = s.height
        s.close

        self.assertTrue(f.get_width_ptr() == expected_w,
                        f"resulting pointer from the final image is : {f.get_width_ptr()} and not {expected_w}")

        # Do another paste just because I feel like it.
        f.paste_thumbnail("./ForHobonichi/test2.png")

    def test_HeightException(self):
        size_in_pixel = hobo.Length_To_Pixel(
            (self.test_width, self.test_height), is_inches=True)

        f = fi.FinalImage("Final_Image.jpg", "./", size_in_pixel)
        f.height_ptr = 10000
        with self.assertRaises(fi.HeightOutOfBoundException):
            f.paste_thumbnail(self.test_thumbnail)
    
    def test_read_settings(self):
        p = hobo.read_printer_settings()
        f = hobo.read_final_image_settings()
        self.assertIsNotNone(p['dpi'])
        self.assertIsNotNone(f['thumbnail']['in_inches'])
        pass


if __name__ == "__main__":
    unittest.main()
