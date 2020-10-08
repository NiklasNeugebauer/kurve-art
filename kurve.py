import numpy as np

class Kurve:
    """ object to represent one kurve
    """
    def __init__(self, pos0, vel0, rot):
        self.pos = pos0
        self.vel = vel0
        self.rot = rot

    def move(self, dt):
        self.pos += np.array([np.sin(self.rot), np.cos(self.rot)]) * self.vel * dt

    def rotate(self, amount):
        self.rot += amount

    def set_vel(self, vel_new):
        self.vel = vel_new

    def set_rot(self, rot_new):
        self.rot = rot_new

    def set_pos(self, pos_new):
        self.pos = pos_new

    def get_pos(self):
        return self.pos

    def get_vel(self):
        return self.vel

    def get_rot(self):
        return self.rot