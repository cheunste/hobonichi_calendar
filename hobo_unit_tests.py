import unittest
import hobonichi_calendar as hobo
import os


class Test_Hobonichi_Calendar(unittest.TestCase):
    def test_calculate_papersize(self):
        self.assertTrue(hobo.Get_PaperSize() == (8.5, 11))

    def test_get_cousin_calendar_size(self):
        self.assertTrue(hobo.Get_Cousin_Calendar_Size() == (3.3, 2.6))

    def test_get_weeks_calendar_size(self):
        self.assertTrue(hobo.Get_Weeks_Calendar_Size() == (2.0, 2.4))

    def test_get_file_type(self):
        self.assertTrue(hobo.Get_Supported_File_Types() == [
                        ("JPEG (*.jpg)", "*.jpg"), ("All files (*.*)", "*.*")])

    def test_convert_paper_to_pixel(self):
        hobo.Convert_To_Pixel((8.5, 11))

    def test_in_cm_convert(self):
        r = hobo.Inches_To_Cm(8.5)
        self.assertTrue(r == 21.59)

    def test_pixel_to_cm(self):
        hobo.Pixel_To_Centimeter(800, 1)

    def test_create_new_image(self):
        p = "./test.jpg"
        hobo.Create_Blank_Image(p, (300, 300))
        r = os.path.exists(p)
        self.assertTrue(r)

    def test_rescale(self):
        hobo.resize("./furret.jpg", "./furrent_rescale.jpg", (150, 150))
        self.assertTrue("./furret_rescale.jpg")

    def test_crop(self):
        size = (490, 140, 930, 720)
        hobo.crop("./furret.jpg", "./furrent_crop.jpg", size)
        self.assertTrue("./furret_crop.jpg")


if __name__ == "__main__":
    unittest.main()
