import pygame
from pygame.locals import *
import numpy
import random

def drawGrid(display, width, height, cellSize):
    # Boucle sur x
    for x in range(0, width, cellSize):
        pygame.draw.line(display, (0, 0, 0), (x, 0),(x, height))
    # Boucle sur y
    for y in range (0, height, cellSize):
        pygame.draw.line(display, (0, 0, 0), (0, y), (width, y))

# Ceci est un commentaire
# sur plusieurs lignes
# utilisé pour tester le profilage
# Et là : c'est un piège !
def populate(width, height, cellSize):
    grid = numpy.zeros((width, height), dtype=numpy.dtype('b'))
    for x in range(width // cellSize):
        for y in range(height // cellSize):
            grid[x, y] = random.randint(0, 1)
    return grid


# Programme principal
if __name__ == '__main__':    
    fps = 10
    window = (640, 480)
    cellSize = 10

    gameOfLife(window, cellSize, fps)
