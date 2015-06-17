__author__ = 'tremity'

from my_color import *


class MyShape(object):
    counter = 0

    def __init__(self, *args, **kwargs):

        self.id = MyShape.counter+1
        self.fill_color = MyColor()  # random color fill
        self.border_color = MyColor(0, 0, 0)  # black border

#        if 'type' in kwargs:
#            self.name = kwargs['type']+str(MyShape.counter)
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'fill_color' in kwargs and isinstance(kwargs['fill_color'], MyColor):
                self.fill_color = kwargs['fill_color']
        if 'border_color' in kwargs and isinstance(kwargs['border_color'], MyColor):
                self.border_color = kwargs['border_color']

        MyShape.counter += 1

    def __del__(self):
        MyShape.counter -= 1

    def __str__(self):
        return self.get_name()

    def __repr__(self):
        return str(self)

    def get_name(self):
        return self.name

    def get_info(self):
        return self.get_name()