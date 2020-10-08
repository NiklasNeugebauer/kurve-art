import pygame as pg
from pygame.locals import *
import numpy as np
import numpy.random

from visualization import KurvenPlotter, PygamePlotter

pg.init()
window = (1000, 1000)
display = pg.display.set_mode(window)

plotter = PygamePlotter(display, 3)
positions = np.array([[0, 250], [0, 500], [0, 750]], dtype=np.float32)
plotter.update_positions(positions, np.arange(3))
plotter.update_colors([[255., 0., 0., 255.], [0., 255., 0., 255.], [0., 0., 255., 255.]])
count = 0
reset = np.array([])

while True:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

    positions[0,0] += 1.
    positions[1,0] += 2.
    positions[2,0] += 5.
    if count % 20 < 5:
        reset = np.arange(3)

    else:
        plotter.update_positions(positions, reset)
        plotter.paint(False)
        pg.display.flip()
        reset = np.array([])
        
    count += 1
    pg.time.wait(10)
    