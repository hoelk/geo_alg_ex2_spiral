__author__ = 'tremity'

import random as rand


class MyColor(object):
    def __init__(self, *args, **kwargs):
        self.r = rand.randint(0,255)  # default to random
        self.g = rand.randint(0,255)  # default to random
        self.b = rand.randint(0,255)  # default to random

        if len(args) == 1:
            if isinstance(args[0], int):
                self.r = self.g = self.b = args[0]
        elif len(args) == 3:
            self.r = args[0]
            self.g = args[1]
            self.b = args[2]

        if all(rgb in kwargs for rgb in ("r", "g", "b")):
            self.r = kwargs['r']
            self.g = kwargs['g']
            self.b = kwargs['b']

    def hex_str(self):
        hex_r = "%0.2X" % self.r
        hex_g = "%0.2X" % self.g
        hex_b = "%0.2X" % self.b
        return "#"+hex_r+hex_g+hex_b

    def get_rgb(self):
        return [self.r, self.g, self.b]