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
    

    def __init__(self, width, height, count):
        self.width, self.height = width, height
        self.count = count
        self.positions = np.array(list(zip(np.zeros(count), np.zeros(count))))
        glViewport(0, 0, width, height)
        glClearColor(0,0,0,0)
        # setup OpenGL to work with arrays instead of individual primitive commands
        glEnableClientState(GL_VERTEX_ARRAY)
        # setup OpenGL to work with arrays instead of individual color commands
        #glEnableClientState(GL_COLOR_ARRAY)

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
        print(lines)
        self.pos_buf = glvbo.VBO(lines)

    def paint(self, clear):
        """ Paint a dot for all data points
        """
        if clear :
            glClear(GL_COLOR_BUFFER_BIT)

        self.pos_buf.bind()

        # mark pos_buf as a specifying vertices
        glVertexPointer(2, GL_FLOAT, 0, self.pos_buf)
        glDrawArrays(GL_LINES, 0, 2 * self.count)
        # TODO use a GL_COLOR_ARRAY for colors

    def getCurrentImage(self):
        # TODO can we use pixel buffer objects for this?
        print("unimplemented!")