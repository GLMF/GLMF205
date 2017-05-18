import pygame
from pygame.locals import *
import numpy
import random
import sys
import math

def drawGrid(display, width, height, cellSize):
    for x in range(0, width, cellSize):
        pygame.draw.line(display, (0, 0, 0), (x, 0),(x, height))
    for y in range (0, height, cellSize):
        pygame.draw.line(display, (0, 0, 0), (0, y), (width, y))

def populate(code, width, height, cellSize):
    grid = numpy.zeros((width, height), dtype=numpy.dtype('b'))
    for y, line in enumerate(code):
        for x, car in enumerate(line):
            if car == '#':
                grid[x, y] = 1
            elif car == ':':
                grid[x, y] = 2
            elif (car == ' ' or car == '\t' or car =='\n') :
                if x == 0:
                    grid[x, y] = 3
                else:
                    grid[x, y] = 4
            else:
                grid[x, y] = 5
    return grid

def displayCells(display, width, height, cellSize, grid, colors):
    for x in range(width // cellSize):
        for y in range(height // cellSize):
            if grid[x, y] != 0:
                pygame.draw.rect(display, colors[grid[x, y]], (x * cellSize, y * cellSize, cellSize, cellSize))
            else:
                pygame.draw.rect(display, (255, 255, 255), (x * cellSize, y * cellSize, cellSize, cellSize))

def initWindow(code, codeName, colors, width=640, height=480, cellSize=10):
    if width % cellSize != 0:
        print('WARNING: width MUST be a multiple of cell size !')
        exit(1)
    if height % cellSize != 0:
        print('WARNING: height MUST be a multiple of cell size !')
        exit(2)
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((width, height)) 
    display.fill((255, 255, 255))
    pygame.display.set_caption('Profilage de ' + codeName) 
    grid = populate(code, width, height, cellSize)
    displayCells(display, width, height, cellSize, grid, colors)
    drawGrid(display, width, height, cellSize)
    return (display, grid, clock)

def applyRules(grid, width, height, cellSize, cellWidth, cellHeight):
    newGrid = numpy.zeros((width, height), dtype=numpy.dtype('b'))
    for x in range(cellWidth):
        for y in range(cellHeight):
            if grid[x, y] == 5 or grid[x, y] == 4:
                if x > 0 and grid[x - 1, y] == 1:
                    newGrid[x, y] = 1
                elif x > 0 and grid[x, y] == 4 and grid[x - 1, y] == 3:
                    newGrid[x, y] = 3
                elif x < cellWidth and grid[x + 1, y] == 2:
                    newGrid[x, y] = 2
                else:
                    newGrid[x, y] = grid[x, y]
            elif grid[x, y] == 2 and x > 0 and grid[x - 1, y] == 1:
                newGrid[x, y] = 1
            else:
                newGrid[x, y] = grid[x, y]
    return newGrid

def profile(code, codeName, colors, window=(640, 480), cellSize=10, fps=10):
    (display, grid, clock) = initWindow(code, codeName, colors, window[0], window[1], cellSize)
    cellWidth = window[0] // cellSize
    cellHeight = window[1] // cellSize

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)

        grid = applyRules(grid, window[0], window[1], cellSize, cellWidth, cellHeight)
        displayCells(display, window[0], window[1], cellSize, grid, colors)
        drawGrid(display, window[0], window[1], cellSize)
        pygame.display.update()    
        clock.tick(fps)

def getWindowSize(code):
    height = len(code)
    width = 0
    for line in code:
        sizeLine = len(line)
        if sizeLine > width:
            width = sizeLine

    return (width * 10, height * 10)


if __name__ == '__main__':    
    if len(sys.argv) != 2:
        print('Syntax : profilage <filename.py>')
        exit(3)

    try:
        with open(sys.argv[1], 'r') as fic:
            code = fic.readlines()
    except:
        print('File error')
        exit(4)

    fps = 10
    window = getWindowSize(code)#(640, 480)
    cellSize = 10
    colors = [
        (255, 255, 255), # blanc
        (211, 211, 211), # gris
        (255, 0, 0), # rouge
        (255, 215, 0), # jaune
        (0, 191, 255), # bleu
        (0, 191, 255), # bleu
    ]

    profile(code, sys.argv[1], colors, window, cellSize, fps)
