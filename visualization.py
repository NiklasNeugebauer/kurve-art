import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.arrays.vbo as glvbo



def square(position, color):
        side_len = 20
        offset = side_len / 2
        glColor(color)
        glBegin(GL_QUADS)
        glVertex2f(position[0] + offset, position[1] + offset)
        glVertex2f(position[0] - offset, position[1] + offset)
        glVertex2f(position[0] - offset, position[1] - offset)
        glVertex2f(position[0] + offset, position[1] - offset)
        glEnd()

class KurvenPlotter:

    def __init__(self, width, height):
        self.width, self.height = width, height
        glViewport(0, 0, width, height)
        glClearColor(0,0,0,0)
        glEnableClientState(GL_VERTEX_ARRAY)

    def update_positions(self, data):
        """ Load new curve positions as a numpy array
        """
        self.data = data
        self.count = data.shape[0]
        self.vbo = glvbo.VBO(self.data)

    def paint(self, clear):
        """ Paint a dot for all data points
        """
        if clear :
            glClear(GL_COLOR_BUFFER_BIT)

        self.vbo.bind()

        glVertexPointer(2, GL_FLOAT, 0, self.vbo)
        glDrawArrays(GL_POINTS, 0, self.count)
        # TODO is there a way to set vertex colors efficiently?

    def getCurrentImage(self):
        # TODO can we use pixel buffer objects for this?
        print("unimplemented!")