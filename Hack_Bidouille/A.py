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

if __name__ == '__main__':
    # Définition de la lettre A
    A = [(3, 1), (4, 1), (2, 2), (5, 2), (2, 3), (5, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (1, 5), (6, 5), (1, 6), (6, 6), (1, 7), (6, 7)]
    # Initialisation des leds en noir
    leds = [Color(0, 0, 0)] * 64

    # Création d'un élément permettant de "manipuler"
    # l'écran de leds
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

    # Initialisation de l'écran
    strip.begin()

    # Ajout de la lettre sur l'écran
    for (x, y) in A:
        leds[x + y * 8] = Color(255, 0, 0)

    # Affichage de l'écran
    displayScreen(strip, leds)

    # Attente de 10s
    time.sleep(10)

    # Effacement de l'écran
    clearScreen(leds)
    displayScreen(strip, leds)
