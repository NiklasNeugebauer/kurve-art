import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random
import itertools

from PIL import Image
from PIL import ImageOps

from visualization import KurvenPlotter, PygamePlotter
from kurve import Kurve

record = True
live = True
record_stride = 50

numKurven = 1000
speed = .1
window = (1000, 1000)
foresight = 10


def position_array(kurven):
    positions = []
    for k in kurven:
        x = k.get_pos()
        positions.append((2 * x[0]/window[0] - 1., 2 * x[1]/window[1] - 1.))
    
    return np.array(positions)

def wiggle(k):
    k.rotate(3.1415/np.random.randint(1, 5))

def not_black(color):
    return color[0] != 0 or color[1] != 0 or color[2] != 0

def oob(koord):
    return koord[0] >= window[0] or koord[0] < 0 or koord[1] >= window[1] or koord[1] < 0

def steer(k, image, dt):
    turn = False
    pos = k.get_pos()
    vel = k.get_vel()
    rot = k.get_rot()
    
    for i in range(int(vel * foresight * dt)):
        koord = ( int(pos[0] + i * np.sin(rot)), int(pos[1] + i * np.cos(rot)) )
        if oob(koord):
            turn = True
            break
        color = image.getpixel(koord)
        if not_black(color):
            turn = True
            break

    if turn:
        dir = np.random.random_integers(0, 2)
        if dir == 0:
            k.rotate(.2)

#def fill(k, display):
#    for x, y in itertools.product([-1, 0, 1], [-1, 0, 1]):
        
if live:
    pg.init()

    display = pg.display.set_mode(window, pg.locals.OPENGL)

plotter = KurvenPlotter(window[0], window[1], numKurven)
kurven = []
for i in range(numKurven):
    posi = (np.random.randint(0, window[0]), np.random.randint(0, window[1]))
    thetai = np.random.randn() * 3.1415
    kurve_new = Kurve(posi, speed, thetai)
    kurven.append(kurve_new)

plotter.update_positions(position_array(kurven), np.arange(numKurven))

cols = np.array(list(zip(.5 * (np.sin(3.1415 * np.arange(numKurven)/numKurven) + np.ones(numKurven)),.5 * (np.sin(1. + 3.1415 * np.arange(numKurven)/numKurven) + np.ones(numKurven)), .5 * (np.sin(2. + 3.1415 * np.arange(numKurven)/numKurven) + np.ones(numKurven)), np.ones(numKurven))))
plotter.update_colors(cols)
count = 0

count = 0
while True:
    if live:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

    data = plotter.getCurrentImage()
    image = Image.frombytes("RGBA", (window[0], window[1]), data)
    #image = ImageOps.flip(image) # in my case image is flipped top-bottom for some reason

    if record and count % record_stride == 0:
        image.save('export/' + str(int(count/record_stride)) + '.png', 'PNG')

    for k in kurven:
        k.move(10)
        wiggle(k)
        
    plotter.update_positions(position_array(kurven), np.array([]))
    plotter.paint(False)

    if live:
        pg.display.flip()

    count += 1
    