from PIL import Image, ImageOps
import tempfile
import os

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]


def main(image_path, output_path):
    is_portrait(image_path)
    Get_Cousin_Calendar_Size()
    paper_size_tuple = Get_PaperSize()
    paper_px = Length_To_Pixel(paper_size_tuple, True)
    hobo_px = Length_To_Pixel(Get_Cousin_Calendar_Size())

    if is_landscape(image_path):
        # if landscape, make the width twice as big and take up two calendar size
        shrink_image(image_path, output_path, (2*hobo_px[0], hobo_px[1]))
    else:
        shrink_image(image_path, output_path, hobo_px)


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


def Length_To_Pixel(paper_size_tuple, is_inches=False):
    (w, h) = paper_size_tuple

    if is_inches:
        w_cm = Inches_To_Cm(w)
        h_cm = Inches_To_Cm(h)
    else:
        w_cm = w
        h_cm = h

    w_px = Centimeter_To_Pixel(w_cm, 1)
    h_px = Centimeter_To_Pixel(h_cm, 1)

    return (w_px, h_px)

# 1in =2.54cm this is convertin


def Inches_To_Cm(i):
    return i*2.54

# Source: https://pixelsconverter.com/pixels-to-centimeters
# But while it is dependent on DPI, 1 cm = 37.79 px


def Pixel_To_Centimeter(px, ppi=1):
    # return px*(2.54/ppi)
    return int(round(px/37.79))


def Centimeter_To_Pixel(cm, ppi):
    return int(round(cm*37.79))


def Create_Blank_Image(output_path, size):
    i = Image.new("RGB", size)
    bg = (255, 255, 255)
    for y in range(size[1]):
        for x in range(size[0]):
            i.putpixel((x, y), bg)
    i.save(output_path, 'PNG', quality=95)


def shrink_image(image_path, output_path, size_px):
    i = Image.open(image_path)
    i.thumbnail(size_px)
    # this adds the border to the shrinked image
    ni = ImageOps.expand(i, 5)
    (w, h) = ni.size
    print(f"shrinked width: {w}, shrinked height: {h}")
    ni.save(output_path, 'PNG', quality=95)


def crop(image_path, output_path, coords):
    i = Image.open(image_path)
    cropped_image = i.crop(coords)
    i.close()
    cropped_image.save(output_path, 'PNG', quality=95)


def is_landscape(image_path):
    i = Image.open(image_path)
    (w, h) = i.size
    print(f"width: {w}, height: {h}")
    i.close()
    return w > h+(h*0.50)


def is_portrait(image_path):
    i = Image.open(image_path)
    (w, h) = i.size
    i.close()
    return h > w


def convert_photos_in_directory(path):
    p = path
    try:
        os.mkdir(f"{p}/ForHobonichi/")
    except Exception as e:
        print("eh?: ", e)
        pass
    for root, dir, files in os.walk(p, topdown=True):
        exclude = set(['ForHobonichi', 'New folder', 'Windows', 'Desktop'])
        dir[:] = [d for d in dir if d not in exclude]
        for file in files:
            input_path = f"{root}{file}"
            output_path = f"{p}ForHobonichi/{file}"
            if file.endswith((".jpeg", ".jpg", ".JPG")):
                print(input_path)
                main(input_path, output_path)


if __name__ == "__main__":
    convert_photos_in_directory("/Users/stephen/Downloads/Photos/")
