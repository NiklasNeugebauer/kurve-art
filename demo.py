import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random

from visualization import KurvenPlotter

pg.init()
window = (1000, 1000)
pg.display.set_mode(window, pg.locals.OPENGL)

plotter = KurvenPlotter(1000, 1000)
positions = np.array([[-1, -.75], [-1., 0], [-1, .75]], dtype=np.float32)

while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    positions[0,0] += .001
    positions[1,0] += .003
    positions[2,0] += .008
    plotter.update_positions(positions)
    plotter.paint(False)
    pg.display.flip()
    pg.time.wait(10)
    