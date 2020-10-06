import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random
import math
import random


pg.init()
window = (1000, 1000)
display = pg.display.set_mode(window)
display.fill((0,0,0))
rand = random.Random()
startPos = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900])
colors = np.array([(255, 255, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0)])
pointColors = []



for i in range(len(startPos)):
    pointColors.append(colors[rand.randint(0,6)])

counterX = 0
counterY = 0
down = True

xIncrease = .01
yIncrease = .5

while True:
    if(counterY > window[1] or counterY < 0):
        down = not(down)
        xIncrease = rand.uniform(0.01, 0.09)
        for i in range(len(pointColors)):
            pointColors[i] = colors[rand.randint(0, 6)]
        if(down):
            yIncrease = rand.uniform(.5, 1.5)
        else:
            yIncrease = -rand.uniform(.5, 1.5)
    counterY += yIncrease


    counterX += xIncrease
    print(math.sin(counterX) * 10)

    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    for i in range(len(startPos)):
        posX = int(startPos[i] + math.sin(counterX) * 100)
        posY = int(counterY)
        Xold = int(startPos[i] + math.sin(counterX-xIncrease) * 100)
        Yold = int(counterY-yIncrease)
        pg.draw.line(display, (255, 255, 255), (posX, posY), (Xold, Yold))
    pg.display.flip()
    pg.time.wait(5)