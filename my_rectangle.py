__author__ = 'tremity'

from my_point import *

class MyRectangle(MyShape):
    counter = 0
    last_auto_name = 0

    def __init__(self, *args, **kwargs):
        self.v0 = MyPoint(name="")  # first corner
        self.v1 = MyPoint(name="")  # second corner (opposite to first)

        if len(args) == 1:
            if isinstance(args[0], MyPoint):
                self.v0 = self.v1 = args[0]
            elif isinstance(args[0], list) or isinstance(args[0], tuple):
                args = args[0]

        if len(args) == 2 and all(isinstance(arg, MyPoint) for arg in args):
            self.v0 = args[0]
            self.v1 = args[1]

        if "name" not in kwargs:
            MyRectangle.last_auto_name += 1
            kwargs['name'] = 'R'+str(MyRectangle.last_auto_name)
        super().__init__(*args, **kwargs)

        #print("Created rectangle with id: " + str(self.id))
        MyRectangle.counter += 1

    def __del__(self):
        MyRectangle.counter -= 1
        #print("Destroyed rectangle with id: " + str(self.id))

    def __str__(self):
        return self.name + "[" + str(self.v0) + ", " + str(self.v1) + "]"

    def __len__(self):
        return 2

    def get_coords(self):
        return [self.v0.get_coords(), self.v1.get_coords()]