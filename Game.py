import numpy as np
import pygame as pg

length, height = 500, 500
black = 0, 0, 0

pg.display.init()
screen = pg.display.set_mode((length, height))
screen.fill(black)

pixelArray = pg.PixelArray(screen)
pixelArray[100:200, 100:200] = (255, 255, 255)
screen.unlock()

screen.blit(pixelArray.surface, (0,0))
