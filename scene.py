import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random

from visualization import KurvenPlotter, PygamePlotter
from kurve import Kurve

numKurven = 2000
speed = .1
window = (1000, 1000)
foresight = 20

def position_array(kurven):
    positions = []
    for k in kurven:
        positions.append(k.get_pos())
    
    return np.array(positions)

def not_black(color):
    return color[0] != 0 or color[1] != 0 or color[2] != 0

def oob(koord):
    return koord[0] >= window[0] or koord[0] < 0 or koord[1] >= window[1] or koord[1] < 0

def steer(k, display, dt):
    turn = False
    pos = k.get_pos()
    vel = k.get_vel()
    rot = k.get_rot()

    
    
    for i in range(int(vel * foresight * dt)):
        koord = ( int(pos[0] + i * np.sin(rot)), int(pos[1] + i * np.cos(rot)) )
        if oob(koord):
            turn = True
            break
        color = display.get_at( koord )
        if not_black(color):
            turn = True
            break

    if turn:
        dir = np.random.random_integers(0, 2)
        if dir == 0:
            k.rotate(.2)

pg.init()

display = pg.display.set_mode(window)

plotter = PygamePlotter(display, numKurven)
kurven = []
for i in range(numKurven):
    posi = (np.random.randint(0, window[0]), np.random.randint(0, window[1]))
    thetai = np.random.randn() * 3.1415
    kurve_new = Kurve(posi, speed, thetai)
    kurven.append(kurve_new)

plotter.update_positions(position_array(kurven), np.arange(numKurven))

cols = np.array(list(zip(255 * .5 * (np.sin(np.arange(numKurven)) + np.ones(numKurven)), 255 * .5 * (np.sin(1. + np.arange(numKurven)) + np.ones(numKurven)), 255 * .5 * (np.sin(2. + np.arange(numKurven)) + np.ones(numKurven)), 255 * np.ones(numKurven))))
#cols = np.array(list(zip(255 * np.ones(numKurven), 255 * np.ones(numKurven), 255 * np.ones(numKurven), 255 * np.ones(numKurven))))
plotter.update_colors(cols)
count = 0

while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    for k in kurven:
        k.move(10)
        steer(k, display, 10)
        
    if count % 200 < 15:
        reset = np.arange(numKurven)

    else:
        plotter.update_positions(position_array(kurven), reset)
        plotter.paint(False)
        reset = np.array([])

    pg.display.flip()
    pg.time.wait(10)
    count += 1

