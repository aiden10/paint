import pyautogui
import time
import os
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
screenshots_folder = os.path.join(CURRENT_DIR, 'screenshots')
file_path = os.path.join(screenshots_folder, 'ghibli.png')

TOP_LEFT = (640, 280)
TOP_RIGHT = (1275, 280)
BOTTOM_LEFT = (640, 910)
BOTTOM_RIGHT = (1275, 910)

def change_color(r, g, b):
    hex = '%02x%02x%02x' % (r, g, b)
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

im = Image.open(file_path)   

width, height = im.size
current_hex = ''
increment_x = (TOP_RIGHT[0] - TOP_LEFT[0]) / width
increment_y = (BOTTOM_LEFT[1] - TOP_LEFT[1]) / height

time.sleep(1)
pyautogui.click((325, 110)) # pencil button

for x in range(0, width, 5):
    for y in range(0, height, 5):
        pixel = im.getpixel((x,y))
        r, g, b = pixel[0], pixel[1], pixel[2]
        
        change_color(r, g, b)
        time.sleep(0.1)
        screen_x = TOP_LEFT[0] + (increment_x * x)
        screen_y = TOP_LEFT[1] + (increment_y * y)
        pyautogui.click((screen_x, screen_y), clicks=5)
        time.sleep(0.5)