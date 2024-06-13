import pyautogui
import time
import os
import math
import random
from PIL import Image

"""
MS Paint Config
    - 512 x 512 pixels
    - 125% zoom

Canvas:
    Top left: 640, 280
    Top right: 1275, 280
    Bottom left: 640, 910
    Bottom right: 1275, 910

Color:
    Edit color button: 1300, 140
    Hex: 1150, 220
    Ok button: 775, 850

Pencil Button: 325, 110

"""
CURRENT_DIR = os.getcwd()
file_name = 'reduced_suika.png'
screenshots_folder = os.path.join(CURRENT_DIR, 'screenshots')
file_path = os.path.join(screenshots_folder, file_name)

TOP_LEFT = (640, 280)
TOP_RIGHT = (1275, 280)
BOTTOM_LEFT = (640, 910)
BOTTOM_RIGHT = (1275, 910)

def reduce_colors(file, num_colors=64):
    with Image.open(os.path.join(screenshots_folder, file)) as img:
        quantized_img = img.convert('P', palette=Image.ADAPTIVE, colors=num_colors)
        
        quantized_img.save(os.path.join(screenshots_folder, 'reduced_'+file))

def change_color(hex):
    pyautogui.click((1300, 140)) # edit color
    time.sleep(0.35)
    pyautogui.click((1150, 220)) # hex text field
    time.sleep(0.35)
    pyautogui.hotkey('ctrl', 'a', 'backspace')
    time.sleep(0.35)
    pyautogui.write(hex)
    pyautogui.click((775, 850))

def get_hex(r, g, b):
    return '%02x%02x%02x' % (r, g, b)

def save(x, y):
    with open('save.txt', 'w') as file:
        file.write(f'File: {file_name}\nX: {x}\nY: {y}')
        file.close()

def load():
    if not os.path.exists('save.txt'):
        return 0, 0
    
    with open('save.txt', 'r') as file:
        data = file.readlines()
        if len(data) < 3:
            return 0, 0
        x = int(data[1].strip().split(': ')[1])
        y = int(data[2].strip().split(': ')[1])
    return x, y

def create_dict(step):
    im = Image.open(file_path).convert('RGB')  
    width, height = im.size
    increment_x = (TOP_RIGHT[0] - TOP_LEFT[0]) / width
    increment_y = (BOTTOM_LEFT[1] - TOP_LEFT[1]) / height
    color_dict = {}
    for x in range(0, width, step):
        for y in range(0, height, step):
            pixel = im.getpixel((x,y))
            r, g, b = pixel[0], pixel[1], pixel[2]
            hex = get_hex(r, g, b)

            screen_x = TOP_LEFT[0] + (increment_x * x)
            screen_y = TOP_LEFT[1] + (increment_y * y)

            coords = (screen_x, screen_y)
            
            if hex in color_dict and hex != 'fefefe' and hex != 'ffffff':
                color_dict[hex].append(coords)
            else:
                color_dict.update({hex: [coords]})
    return color_dict


def change_size():
    pyautogui.moveTo(37, 715)
    move = random.randint(20, 70)
    pyautogui.click((37, 715 + move))

def quick_print(step):
    time.sleep(1)
    pyautogui.click((325, 110)) # pencil button

    pixel_dict = create_dict(step)
    for hex in pixel_dict:
        change_color(hex)
        for coords in pixel_dict[hex]:
            pyautogui.click((coords[0], coords[1]), clicks=5)

def main(style):
    im = Image.open(file_path)   

    width, height = im.size
    step = 10
    total_pixels = width * height
    current_hex = ''
    color_changed = False
    increment_x = (TOP_RIGHT[0] - TOP_LEFT[0]) / width
    increment_y = (BOTTOM_LEFT[1] - TOP_LEFT[1]) / height

    saved_x, saved_y = load()

    time.sleep(1)
    pyautogui.click((325, 110)) # pencil button

    for x in range(saved_x, width, step):
        start_y = saved_y if x == saved_x else 0
        for y in range(start_y, height, step):
            save(round(x), round(y))
            pixel = im.getpixel((x,y))
            r, g, b = pixel[0], pixel[1], pixel[2]
            hex = get_hex(r, g, b)
            if hex == 'FEFEFE' or hex == 'FFFFFF':
                continue
            if current_hex != hex:
                change_color(hex)
                color_changed = True
                time.sleep(0.1)
            else: 
                color_changed = False

            screen_x = TOP_LEFT[0] + (increment_x * x)
            screen_y = TOP_LEFT[1] + (increment_y * y)
            change_size()

            if style == 'dots':
                pyautogui.click((screen_x, screen_y), clicks=5)
            elif style == 'lines':
                pyautogui.moveTo(screen_x, screen_y)
                pyautogui.click()
                pyautogui.dragTo(TOP_RIGHT[0], screen_y, 0.1, button='left')
            elif style == 'circles':
                for i in range(0,10):
                    j = (((i/10)*2)*math.pi)
                    x = math.cos(j) 
                    y = math.sin(j) 
                    pyautogui.dragTo(screen_x/2 + (screen_y/3)*x
                            ,screen_y/2 + (screen_y/3)*y, duration=1, button='left')
                    
            current_hex = hex

            total_drawn = x * y
            print(f'Percentage Drawn: {round((total_drawn/total_pixels) * 100, 2)}%')

    open('save.txt', 'w').close() # clear file

# main('dots')
quick_print(10)
# reduce_colors('jojo.png', num_colors=2)
