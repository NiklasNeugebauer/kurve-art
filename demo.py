import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random as rdn

from visualization import KurvenPlotter

pg.init()
window = (1000, 1000)
pg.display.set_mode(window, OPENGL)

plotter = KurvenPlotter(1000, 1000)


while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
    positions = np.array(.2*rdn.randn(100000,2),dtype=np.float32)
    plotter.load_positions(positions)
    plotter.paintCurrent(False)
    pg.display.flip()
    pg.time.wait(10)
    