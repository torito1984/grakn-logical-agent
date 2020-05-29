# The hoover environment is made up of everything that does not live 
# in the logic world of the agent: positions, dirt, sensors, actuators, people walking, coronavirus, ...
#
# What the agent knows about the world is what you have set up him to know, but this will be always be extensible

import numpy as np
import random

def rand_bin_array(K, N, M):
    dd = np.zeros((N, M))
    dd[:K, :K]  = 1
    dd = dd.ravel()
    np.random.shuffle(dd)
    dd = dd.reshape(N,M)
    return dd

class Environment:

    def __init__(self, K=2, N=9, M=9):
        # Initiate grid or dirt
        self.dirty = rand_bin_array(K, N, M)
        self.N = N
        self.M = M
        # Initiate random position of the wumpus
        self.hoover_x = random.randint(0, N-1)
        self.hoover_y = random.randint(0, M-1)
        # where are we pointing
        self.pointings = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        self.hoover_p = random.randint(0, 7)

    def advance(self):
        print("Advance")
        self.hoover_x = max(0, min(self.N-1, self.hoover_x + self.pointings[self.hoover_p][0]))
        self.hoover_y = max(0, min(self.M-1, self.hoover_y + self.pointings[self.hoover_p][1]))

    def rotate_right(self):
        print("Rotating right")
        self.hoover_p = (self.hoover_p + 1) % 8

    def rotate_left(self):
        print("Rotating left")
        self.hoover_p = (self.hoover_p - 1) % 8

    def clean(self):
        print("Cleaning position {}, {}".format(self.hoover_x, self.hoover_y))
        self.dirty[self.hoover_x,self.hoover_y] = 0

    def is_clean(self, x, y):
        return self.dirty[self.hoover_x, self.hoover_y] == 0

    def get_position(self):
        return (self.hoover_x, self.hoover_y)

    def get_pointing(self):
        return self.pointings[self.hoover_p]

    def state(self):
        dd = self.dirty.copy()
        dd[self.hoover_x, self.hoover_y] = -(self.hoover_p+1)
        return dd

    def finished(self):
        return self.dirty.sum().sum() == 0

    def can_advance(self):
        prospect_x = self.hoover_x + self.pointings[self.hoover_p][0]
        prospect_y = self.hoover_y + self.pointings[self.hoover_p][1]

        return prospect_x >=0 and prospect_x < self.N and prospect_y >=0 and prospect_y < self.M


