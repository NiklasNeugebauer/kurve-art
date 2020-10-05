import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

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
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, 1, -1, -1, 1)

    def load_positions(self, data):
        """ Load new curve positions as a numpy array
        """
        self.data = data
        self.count = data.shape[0]

    def paintCurrent(self):
        """ Paint a dot at all current positions
        """
        self.vbo.bind()
        glEnableClientState(gl.GL_VERTEX_ARRAY)
        glVertexPointer(2, gl.GL_FLOAT, 0, self.vbo)
        glDrawArrays(gl.GL_POINTS, 0, self.count)
        # TODO is there a way to set vertex colors efficiently?

    def getCurrentImage(self):
        # TODO can we use pixel buffer objects for this?
        print("unimplemented!")