import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random

from visualization import KurvenPlotter, PygamePlotter
from kurve import Kurve

numKurven = 1000
speed = .1


def position_array(kurven):
    positions = []
    for k in kurven:
        positions.append(k.get_pos())
    
    return np.array(positions)

def steer(k, kurven):
    k.rotate(np.random.random() * 3.1415)

pg.init()
window = (1000, 1000)
display = pg.display.set_mode(window)

plotter = PygamePlotter(display, numKurven)
kurven = []
for i in range(numKurven):
    posi = (np.random.randint(0, window[0]), np.random.randint(0, window[1]))
    thetai = np.random.randn() * 3.1415
    kurve_new = Kurve(posi, speed, thetai)
    kurven.append(kurve_new)

plotter.update_positions(position_array(kurven), np.arange(numKurven))

cols = np.array(list(zip(255 * .5 * (np.sin(3.1415 * np.arange(numKurven)/numKurven) + np.ones(numKurven)), 255 * .5 * (np.sin(1. + 3.1415 * np.arange(numKurven)/numKurven) + np.ones(numKurven)), 255 * .5 * (np.sin(2. + 3.1415 * np.arange(numKurven)/numKurven) + np.ones(numKurven)), 255 * np.ones(numKurven))))
plotter.update_colors(cols)

while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    for k in kurven:
        k.move(10)
        steer(k, kurven)
        
    
    plotter.update_positions(position_array(kurven), np.array([]))
    plotter.paint(False)
    pg.display.flip()
    pg.time.wait(10)

