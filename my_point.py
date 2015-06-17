__author__ = 'tremity'

from my_shape import *
from math import *
from my_constants import *


class MyPoint(MyShape):
    counter = 0
    last_auto_name = 0

    def __init__(self, *args, **kwargs):
        self.x = 0.0
        self.y = 0.0

        #print("MyPoint has " + str(len(args)) + " args:" + str(args))
        if len(args) == 1:
            if isinstance(args[0], int) or isinstance(args[0], float):
                self.x = self.y = float(args[0])
            elif isinstance(args[0], list) or isinstance(args[0], tuple):
                args = args[0]

        if len(args) == 2 and all(any(isinstance(arg, num_type) for num_type in (int, float)) for arg in args):
            self.x = float(args[0])
            self.y = float(args[1])

        if "name" not in kwargs:
            MyPoint.last_auto_name += 1
            kwargs['name'] = 'p'+str(MyPoint.last_auto_name)
        super().__init__(*args, **kwargs)

        #print("Created point with id: " + str(self.id))
        MyPoint.counter += 1

    def __del__(self):
        MyPoint.counter -= 1
        #print("Destroying point with id: " + str(self.id))

    def __str__(self):
        return self.get_name() + self.get_coords_str()

    def __len__(self):
        return 1

    def dist(self, p):
        return sqrt((self.x-p.x)**2 + (self.y-p.y)**2)

    def get_coords(self):
        return [self.x, self.y]

    def get_coords_str(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def get_info(self):
        return self.get_name() + ":\n" \
                "- Coordinates:" + str(self.get_coords_str())

    def pt_pos(self, p1, p2):
        if isinstance(p1, MyPoint) and isinstance(p2, MyPoint):
            z_mod = (p2.x - p1.x) * (self.y - p1.y) - (self.x - p1.x) * (p2.y - p1.y)
            if z_mod == 0:
                #return COLLINEAR
                if p1.dist(p2) == self.dist(p1) + self.dist(p2):
                    return BETWEEN
                elif self.dist(p1) < self.dist(p2):
                    return BEFORE
                else:
                    return AFTER
            elif z_mod > 0:
                return LEFT
            else:
                return RIGHT

    def __sub__(self, other):
        if isinstance(other, MyPoint):
            return MyPoint(self.x-other.x, self.y-other.y, name="")

        return MyPoint(self.x, self.y, name="")

    def __add__(self, other):
        if isinstance(other, MyPoint):
            return MyPoint(self.x+other.x, self.y+other.y, name="")

        return MyPoint(self.x, self.y, name="")

    def __eq__(self, other):
        if isinstance(other, MyPoint) and self.x == other.x and self.y == other.y:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def cross_product(self, other):
        if isinstance(other, MyPoint):
            return self.x * other.y - self.y * other.x
        return False

#p0 = MyPoint(0,0)
#p1 = MyPoint(1,1)
#p2 = MyPoint(1,0)
#p3 = MyPoint(2,2)
#p4 = p0+p1
#print(str(p4))

#pos = p1.pt_pos(p0,p3)

#print(pos)
