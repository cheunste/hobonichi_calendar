from PIL import Image, ImageOps
import tempfile
import os
import FinalImage as fi
import copy
import yaml

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
temp_name = 'ForHobonichi'

def convert_photos_in_directory(path):
    p = path
    try:
        os.mkdir(f"{p}/{temp_name}/")
    except Exception as e:
        print("eh?: ", e)
        pass
    for root, dir, files in os.walk(p, topdown=True):
        exclude = set([f'{temp_name}', 'New folder', 'Windows', 'Desktop'])
        dir[:] = [d for d in dir if d not in exclude]
        for file in files:
            input_path = f"{root}{file}"
            output_path = f"{p}{temp_name}/{file}"
            if file.endswith((".jpeg", ".jpg", ".JPG")):
                print(input_path)
                setup(input_path, output_path)

    size_in_pixel = Length_To_Pixel(Get_PaperSize(), is_inches=True)
    paste_thumbnails(p, size_in_pixel)

def setup(image_path, output_path):
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



def paste_thumbnails(p, size_in_pixel):
    id = 0
    f = fi.FinalImage(f"Final_Print{id}.jpg", f"{p}", size_in_pixel)
    t = copy.deepcopy(f.get_all_thumbnails(f"{p}{temp_name}", temp_name))
    for thumbnail_path in t:
        try:
            f.paste_thumbnail(thumbnail_path)
        except fi.HeightOutOfBoundException:
            # Create a new Image
            id += 1
            new_f = fi.FinalImage(f"Final_Print{id}.jpg", p, size_in_pixel)
            f = new_f

# Warning, the 8.5 x 11 is in inches. No idea what the default metric size is for printer paper


def Get_PaperSize(paper=(8.5, 11)):
    p = read_printer_settings()
    return (p['paper_width'],p['paper_height'])


def Get_Cousin_Calendar_Size():
    # Warning, the size here is in cm
    f  = read_final_image_settings()
    return (f['thumbnail']['width'],f['thumbnail']['height'])


def Get_Supported_File_Types():
    return file_types


def Length_To_Pixel(paper_size_tuple, is_inches=False):
    (w, h) = paper_size_tuple
    ppi = read_printer_settings()['ppi']

    if is_inches:
        w_cm = Inches_To_Cm(w)
        h_cm = Inches_To_Cm(h)
    else:
        w_cm = w
        h_cm = h

    w_px = Centimeter_To_Pixel(w_cm, ppi)
    h_px = Centimeter_To_Pixel(h_cm, ppi)

    return (w_px, h_px)

# 1in =2.54cm this is convertin


def Inches_To_Cm(i):
    return i*2.54

# From : https://pixelsconverter.com/pixels-to-centimeters
# 1 cm = 96px/2.54 =37.79 px,but it is also dependent on DPI
# Note that it 1 px = 1 dot, so 300 DPI = 300 px 


def Pixel_To_Centimeter(px, ppi=1):
    return int(round(px*(2.54/ppi)))


def Centimeter_To_Pixel(cm, ppi):
    return int(round(cm/(2.54/ppi)))


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

    border = read_final_image_settings()['border']
    # this adds the border to the shrinked image
    ni = ImageOps.expand(i, border)
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


def put_all_images_to_final_print():
    pass

def read_printer_settings():
    with open("./config.yaml",'r') as f:
        x = yaml.load(f,Loader=yaml.FullLoader)
    return x['printer']

def read_final_image_settings():
    with open("./config.yaml",'r') as f:
        x = yaml.load(f,Loader=yaml.FullLoader)
    return x['final_image']



if __name__ == "__main__":
    d = input("Please entire a directory with images (ie. /Users/Alex/Photos):")
    convert_photos_in_directory(d)
