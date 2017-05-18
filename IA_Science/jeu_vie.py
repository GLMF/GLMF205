import pygame
from pygame.locals import *
import numpy
import random

def drawGrid(display, width, height, cellSize):
    for x in range(0, width, cellSize):
        pygame.draw.line(display, (0, 0, 0), (x, 0),(x, height))
    for y in range (0, height, cellSize):
        pygame.draw.line(display, (0, 0, 0), (0, y), (width, y))

def populate(width, height, cellSize):
    grid = numpy.zeros((width, height), dtype=numpy.dtype('b'))
    for x in range(width // cellSize):
        for y in range(height // cellSize):
            grid[x, y] = random.randint(0, 1)
    return grid

def displayCells(display, width, height, cellSize, grid, color=(255, 155, 0)):
    for x in range(width // cellSize):
        for y in range(height // cellSize):
            if grid[x, y] == 1:
                pygame.draw.rect(display, color, (x * cellSize, y * cellSize, cellSize, cellSize))
            else:
                pygame.draw.rect(display, (255, 255, 255), (x * cellSize, y * cellSize, cellSize, cellSize))

def initWindow(width=640, height=480, cellSize=10):
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
    pygame.display.set_caption('Jeu de la Vie') 
    grid = populate(width, height, cellSize)
    displayCells(display, width, height, cellSize, grid)
    drawGrid(display, width, height, cellSize)
    return (display, grid, clock)

def getNeighbours(grid, cell, cellWidth, cellHeight):
    neighbours = 0
    for mod_x in range (-1, 2):
        for mod_y in range (-1, 2):
            if mod_x == 0 and mod_y == 0:
                continue
            neighbourCell = (cell[0] + mod_x, cell[1] + mod_y)
            if (neighbourCell[0] < cellWidth  and neighbourCell[0] >= 0) and \
               (neighbourCell [1] < cellHeight and neighbourCell[1] >= 0) and \
               grid[neighbourCell[0], neighbourCell[1]] == 1:
                        neighbours += 1
    return neighbours

def applyRules(grid, width, height, cellSize, cellWidth, cellHeight):
    newGrid = numpy.zeros((width, height), dtype=numpy.dtype('b'))
    for x in range(cellWidth):
        for y in range(cellHeight):
            nbNeighbours = getNeighbours(grid, (x, y), cellWidth, cellHeight)
            if grid[x, y] == 1:
                if nbNeighbours < 2:
                    newGrid[x, y] = 0
                elif nbNeighbours > 3:
                    newGrid[x, y] = 0
                else:
                    newGrid[x, y] = 1
            else:
                if nbNeighbours == 3:
                    newGrid[x, y] = 1
                # else:
                    # newGrid[x, y] = 0
    return newGrid

def gameOfLife(window=(640, 480), cellSize=10, fps=10):
    (display, grid, clock) = initWindow(window[0], window[1], cellSize)
    cellWidth = window[0] // cellSize
    cellHeight = window[1] // cellSize

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit(0)

        grid = applyRules(grid, window[0], window[1], cellSize, cellWidth, cellHeight)
        displayCells(display, window[0], window[1], cellSize, grid)
        drawGrid(display, window[0], window[1], cellSize)
        pygame.display.update()    
        clock.tick(fps)


if __name__ == '__main__':    
    fps = 10
    window = (640, 480)
    cellSize = 10

    gameOfLife(window, cellSize, fps)
