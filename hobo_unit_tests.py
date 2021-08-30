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

    def test_in_cm_convert(self):
        r = hobo.Inches_To_Cm(8.5)
        self.assertTrue(r == 21.59)

    def test_pixel_to_cm(self):
        #self.assertTrue(hobo.Pixel_To_Centimeter(800) == 2032.0)
        #self.assertTrue(hobo.Pixel_To_Centimeter(800, 5) == 406.4)
        self.assertTrue(hobo.Pixel_To_Centimeter(800) == 21)

    def test_cm_to_pixel(self):
        self.assertTrue(hobo.Centimeter_To_Pixel(1, 2) == 38)

    def test_create_new_image(self):
        p = "./test.jpg"
        hobo.Create_Blank_Image(p, (300, 300))
        r = os.path.exists(p)
        self.assertTrue(r)

    def test_rescale(self):
        hobo.resize("./furret.jpg", "./furrent_rescale.jpg", (150, 150))
        self.assertTrue("./furret_rescale.jpg")

        print(hobo.Length_To_Pixel(hobo.Get_Cousin_Calendar_Size()))
        hobo.resize("./furret.jpg", "./furrent_rescale2.jpg",
                    hobo.Length_To_Pixel(hobo.Get_Cousin_Calendar_Size()))
        self.assertTrue("./furret_rescale2.jpg")

    def test_crop(self):
        size = (490, 140, 930, 720)
        hobo.crop("./furret.jpg", "./furrent_crop.jpg", size)
        self.assertTrue("./furret_crop.jpg")

    def test_landscape_or_portrait(self):
        self.assertTrue(hobo.is_landscape("./surfing_pikachu.jpg"))
        self.assertFalse(hobo.is_portrait("./surfing_pikachu.JPG"))


if __name__ == "__main__":
    unittest.main()
