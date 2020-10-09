import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.arrays.vbo as glvbo

import pygame as pg
from pygame.locals import *

def square(position, color):
        side_len = .1
        offset = side_len / 2
        glColor(color)
        glBegin(GL_QUADS)
        glVertex2f(position[0] + offset, position[1] + offset)
        glVertex2f(position[0] - offset, position[1] + offset)
        glVertex2f(position[0] - offset, position[1] - offset)
        glVertex2f(position[0] + offset, position[1] - offset)
        glEnd()

class PygamePlotter:
    def __init__(self, window, count):
        self.window = window
        self.count = count

        self.positions = np.array(list(zip(np.zeros(count), np.zeros(count))), dtype=np.float32)
        self.colors = np.array(list(zip(np.ones(count), np.ones(count), np.ones(count), np.ones(count))))

    def update_positions(self, data, reset):
        """ Load new curve positions as a numpy array of format [x, y]
            The new position will be drawn disconnected if its index is in reset
            ex. update_positions(np.array([1,1],[0,0]), [1]) will connect the first line to (1,1), but start a new line at (0,0)
        """
        # copy last positions
        last_positions = self.positions.copy()
        self.positions = np.require(data.copy(),np.float32,'F')
        # reset lines where requested by placing its start at the new position, too
        for i in reset:
            last_positions[i] = data[i]
        
        # interlace positions with last_positions (format used by opengl is [start1, end1, start2, end2, ...])
        lines = np.array([(val[0], val[1]) for pair in zip(last_positions, self.positions) for val in pair], dtype=np.float32)
        self.pos_buf = lines

    def update_colors(self, data):
        """ load new colors as a full numpy array of format [[r, g, b, a]]
        """
        self.colors = data.copy()

        # interlace colors with their old counterparts as there will be 2 vertices per line
        pairs = np.array([val for pair in zip(self.colors, self.colors) for val in pair], dtype=np.float32)
        self.col_buf = pairs

    def paint(self, clear):
        """ Paint a line for all data points
        """
        if clear :
            self.window.fill((255,255,255))

        for i in range(0, self.count, 1):
            pg.draw.line(self.window, self.colors[i], self.pos_buf[2*i], self.pos_buf[2*i+1])

    def getCurrentImage(self):
        # TODO can we use pixel buffer objects for this?
        print("unimplemented!")

class KurvenPlotter:
    

    def __init__(self, width, height, count):
        self.width, self.height = width, height
        self.count = count
        self.positions = np.array(list(zip(np.zeros(count), np.zeros(count))))
        self.update_positions(self.positions, [])
        self.colors = np.array(list(zip(np.ones(count), np.ones(count), np.ones(count), np.ones(count))))
        self.update_colors(self.colors)
        glViewport(0, 0, width, height)
        glClearColor(0,0,0,0)
        # setup OpenGL to work with arrays instead of individual primitive commands
        glEnableClientState(GL_VERTEX_ARRAY)
        # setup OpenGL to work with arrays instead of individual color commands
        glEnableClientState(GL_COLOR_ARRAY)

    def update_positions(self, data, reset):
        """ Load new curve positions as a numpy array of format [x, y]
            The new position will be drawn disconnected if its index is in reset
            ex. update_positions(np.array([1,1],[0,0]), [1]) will connect the first line to (1,1), but start a new line at (0,0)
        """
        # copy last positions
        last_positions = self.positions.copy()
        self.positions = data.copy()
        # reset lines where requested by placing its start at the new position, too
        for i in reset:
            last_positions[i] = data[i]
        
        # interlace positions with last_positions (format used by opengl is [start1, end1, start2, end2, ...])
        lines = np.array([val for pair in zip(last_positions, self.positions) for val in pair], dtype=np.float32)
        self.pos_buf = glvbo.VBO(lines)

    def update_colors(self, data):
        """ load new colors as a full numpy array of format [[r, g, b, a]]
        """
        self.colors = data

        # interlace colors with their old counterparts as there will be 2 vertices per line
        pairs = np.array([val for pair in zip(self.colors, self.colors) for val in pair], dtype=np.float32)
        self.col_buf = glvbo.VBO(pairs)

    def paint(self, clear):
        """ Paint a line for all data points
        """
        if clear :
            glClear(GL_COLOR_BUFFER_BIT)


        self.col_buf.bind()
        # mark col_buf as specifying vertex_colors
        glColorPointer(4, GL_FLOAT, 0, self.col_buf)
        # unbind the buffer to make room for positions
        self.col_buf.unbind()

        self.pos_buf.bind()
        # mark pos_buf as a specifying vertices
        glVertexPointer(2, GL_FLOAT, 0, self.pos_buf)
        # unbin the buffer just in case
        self.pos_buf.unbind()
        
        glDrawArrays(GL_LINES, 0, 2 * self.count)

    def getCurrentImage(self):
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        return glReadPixels(0, 0, self.width, self.height, GL_RGBA, GL_UNSIGNED_BYTE)