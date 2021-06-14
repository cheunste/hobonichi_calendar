from PIL import Image
import tempfile

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


def main():
    return


# Warning, the 8.5 x 11 is in inches. No idea what the default metric size is for printer paper
def Get_PaperSize(paper=(8.5, 11)):
    return paper


def Get_Cousin_Calendar_Size():
    # Warning, the size here is in cm
    return (3.3, 2.6)


def Get_Weeks_Calendar_Size():
    # Warning, the size here is in cm
    return (2.0, 2.4)


def Get_Supported_File_Types():
    return file_types


def Convert_To_Pixel(paper_size_tuple):
    (w, h) = paper_size_tuple

    w_cm = Inches_To_Cm(w)
    h_cm = Inches_To_Cm(h)

    w_px = Centimeter_To_Pixel(w_cm, 1)
    h_px = Centimeter_To_Pixel(h_cm, 1)

    print(f"width is {w_px} px and height is {h_px} px")


# 1in =2.54cm this is convertin
def Inches_To_Cm(i):
    return i*2.54


def Pixel_To_Centimeter(px, ppi):
    return px*(2.54/ppi)


def Centimeter_To_Pixel(cm, ppi):
    return (cm/ppi)


def Create_Blank_Image(output_path, size):
    image = Image.new("RGB", size)
    white = (255, 255, 255)
    for y in range(size[1]):
        for x in range(size[0]):
            image.putpixel((x, y), white)
    image.save(output_path)


def resize(image_path, output_path, size):
    image = Image.open(image_path)
    resized_image = image.resize(size)
    resized_image.save(output_path)


def crop(image_path, output_path, coords):
    image = Image.open(image_path)
    cropped_image = image.crop(coords)
    cropped_image.save(output_path)


if __name__ == "__main__":
    main()
