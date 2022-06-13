import sys
from typing import List, TypedDict
from PIL import Image
from math import sqrt

from os import listdir
from os.path import isfile, join

class RGB(TypedDict):
    r: int
    g: int
    b: int


def get_pixels(image: Image.Image) -> List[RGB]:
    rgb_im = image.convert('RGB')
    width, height = rgb_im.size

    pixels_list: List[RGB] = []
    for i in range(width):
        for j in range(height):
            r, g, b = rgb_im.getpixel((i, j))
            rgb: RGB = {'r': r, 'g': g, 'b': b}
            pixels_list.append(rgb)
    return pixels_list


def get_avg(img: Image.Image) -> RGB:
    pixels = get_pixels(img)

    r, g, b = 0, 0, 0
    for rgb in pixels:
        r+=rgb.get('r')
        g+=rgb.get('g')
        b+=rgb.get('b')
    print('average calculated successfully')

    return {'r': r//len(pixels), 'g': g//len(pixels), 'b': b//len(pixels)}


def open_from_path(path: str) -> Image.Image:
    return Image.open(path)

def open_from_dir(directory: str) -> List[Image.Image]:
    return [open_from_path(directory + '/' + file) for file in [f for f in listdir(directory) if isfile(join(directory, f))]]

def close_all(imgs: List[Image.Image]):
    [img.close() for img in imgs]


def get_nearest(average_image_rgb: RGB, average_image_rgbs: List[RGB]) -> RGB:
    nearest = average_image_rgbs[0]
    best_dist = float("inf")

    for rgbs in average_image_rgbs:
        dist = sqrt( (average_image_rgb.get('r') - rgbs.get('r'))**2 + (average_image_rgb.get('g') - rgbs.get('g'))**2 + (average_image_rgb.get('b') - rgbs.get('b'))**2 )
        if dist < best_dist:
            best_dist = dist
            nearest = rgbs
            print(best_dist)
        
    return nearest

def resize(img: Image.Image, size:tuple[int, int]) -> Image.Image:
    return img.resize(size)

def resize_all(images: List[Image.Image], size: tuple[int, int]) -> List[Image.Image]:
    return [resize(img, size) for img in images]

def create(img_path: str, dir_path: str, size: int, out: str):
    img = open_from_path(img_path)
    img_w, img_h = img.size

    images = open_from_dir(dir_path)
    resized = resize_all(images, (size, size))

    images_rgb_avgs = [get_avg(img) for img in resized]



    background = Image.new('RGB', (img_w, img_h), (0, 0, 0))
    print("following amount of images will be put together (x, y): ")
    print(img_h // size + img_h % size, img_w // size + img_w % size)
    
    ite = 0
    for i in range(0, img_w, size):
        for j in range(0, img_h, size):
            area = (i, j, i+size, j+size)
            sub_img = img.crop(area)
            nearest = get_nearest(get_avg(sub_img), images_rgb_avgs)
            background.paste(resized[images_rgb_avgs.index(nearest)], (i, j))
            print("position: ")
            print(i, j)
            ite+=1

    print("Total number of iterations: ")
    print(ite)

    background.save(out)
    close_all(images)
    img.close()


create(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4])
