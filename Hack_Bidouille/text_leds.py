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
    y = 0
    for row in range(size[0]):
        x = 0
        for col in range(size[1] * (num - 1), size[1] * num):
            if array[row, col] == 1:
                leds[x + y * 8] = color
            else:
                leds[x + y * 8] = Color(0, 0, 0)
            x += 1
        y += 1
    return leds


if __name__ == '__main__':
    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64

    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

    # Initialisation de l'écran
    strip.begin()

    image = text2image('LINUX MAGAZINE')
    arr = image2array(image)

    for i in range(int(np.shape(arr)[1] / 7)):
        leds = draw_letter(leds, arr, (8, 7), i + 1, Color(255, 0, 0))
        # Affichage de l'écran
        displayScreen(strip, leds)
        # Attente de 1s
        time.sleep(1)

    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)
