from PIL import Image, ImageFont, ImageDraw
import numpy as np
from vrtneopixel import *
import time

# Variables de configuration de l'écran
LED_COUNT = 64
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 8
LED_INVERT = False

def clearScreen(leds):
    for i in range(64):
        leds[i] = Color(0, 0, 0)

def displayScreen(strip, leds):
    for i in range(64):
        strip.setPixelColor(i, leds[i])
    strip.show()

def text2image(text, fontName='Hack-Regular.ttf', pt=11, saveName=None):
    font = ImageFont.truetype(fontName, pt)
    (w, h) = font.getsize(text)
    image = Image.new('L', (w, h), 1)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
    if not saveName is None:
        image.save(saveName)
    return image

def image2array(image):
    arr = np.asarray(image)
    arr = np.where(arr, 0, 1)
    arr = arr[(arr != 0).any(axis=1)]
    arr = np.concatenate((np.zeros((8, 7)), arr), axis=1)
    arr = np.concatenate((arr, np.zeros((8, 7))), axis=1)
    return arr

def draw_letter(leds, array, size, num, color):
    array = array[:, size[1] * (num - 1) : size[1] * num]
    for row in range(size[0]):
        for col in range(size[1]):
            if array[row, col] == 1:
                leds[col + row * 8] = color
            else:
                leds[col + row * 8] = Color(0, 0, 0)
    return leds

def draw_part(leds, array, start, stop, color, filter_effect=None):
    array = array[:, start : stop]
    for row in range(8):
        for col in range(8):
            if array[row, col] == 1:
                if filter_effect is None:
                    leds[col + row * 8] = color
                else:
                    leds[col + row * 8] = filter_effect[col + row * 8]
            else:
                leds[col + row * 8] = Color(0, 0, 0)
    return leds

def scroll_h(strip, leds, text, color, filter_effect=None):
    image = text2image(text)
    arr = image2array(image)

    for start in range(0, np.shape(arr)[1] - 7):
        leds = draw_part(leds, arr, start, start + 8, color, filter_effect)
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 0,2s
        time.sleep(0.2)

def get_letter(array, size, num):
    letter = array[:, size[1] * (num - 1) : size[1] * num]
    letter = np.concatenate((letter, np.zeros((1, 7))), axis=0)
    return letter

def verticalize(array, size):
    new_array = np.zeros((size[1], size[0]))
    for i in range(int(np.shape(array)[1] / 7)):
        print(i, ' ', get_letter(array, (8, 7), i + 1))
        new_array[i * 9 : (i + 1) * 9, 0:7] = get_letter(array, (8, 7), i + 1)
    return new_array

def draw_part_v(leds, array, start, stop, color):
    array = array[start:stop, :]
    for row in range(8):
        for col in range(8):
            if array[row, col] == 1:
                leds[col + row * 8] = color
            else:
                leds[col + row * 8] = Color(0, 0, 0)
    return leds

def scroll_v(strip, leds, text, color):
    image = text2image(text)
    arr = image2array(image)
    arr = verticalize(arr, (np.shape(arr)[0], (len(text) + 2) * 8 + len(text) + 2))
    
    for start in range(0, np.shape(arr)[0] - 8):
        leds = draw_part_v(leds, arr, start, start + 8, color)
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 0,2s
        time.sleep(0.2)

if __name__ == '__main__':
    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64

    # Initialisation du filtre d'effet
    filter_effect = [Color(120 + 2 * i, i, i) for i in range(64)]

    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

    # Initialisation de l'écran
    strip.begin()

    scroll_h(strip, leds, 'LINUX MAGAZINE', Color(255, 0, 0), filter_effect)

    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)
