__author__ = 'tremity'

from my_shape import *
from my_point import *


class MyLine(MyShape):
    counter = 0
    last_auto_name = 0

    def __init__(self, *args, **kwargs):
        self.vertices = []

        #print(str(args))

        if len(args) > 0:
            self.add_vertices(args)

        if 'vertices' in kwargs:
            self.add_vertices(kwargs['vertices'])

        if "name" not in kwargs:
            MyLine.last_auto_name += 1
            kwargs['name'] = 'L'+str(MyLine.last_auto_name)
        super().__init__(*args, **kwargs)

        #print("Created line with id: " + str(self.id))
        MyLine.counter += 1

    def __del__(self):
        MyLine.counter -= 1
        #print("Destroying line with id: " + str(self.id))

    def __str__(self):
        return self.get_name() + self.get_coords_str()

    def __len__(self):
        return len(self.vertices)

    def add_vertices(self, vs, anonymous=True):
        for v in vs:
            if len(v) == 2 and all(any(isinstance(coord, num_type) for num_type in (int, float)) for coord in v):
                #print(str(v))
                self.add_vertex(MyPoint(v[0], v[1], name=""))
            elif len(v) == 1 and isinstance(v, MyPoint):
                self.add_vertex(v, anonymous)

    def add_vertex(self, p, anonymous=True):
        if not isinstance(p, MyPoint):
            p = MyPoint(p, name="")  # create and anonymous point

        if isinstance(p, MyPoint):
            if p.name and anonymous and p.name != "": # if it is not an anonymous point
                p = MyPoint(p.x, p.y, name="")  # create a copy that is anonymous
            self.vertices.append(p)

    def pop_vertex(self):
        return self.vertices.pop()

    def get_coords(self):
        coords = []
        for v in self.vertices:
            coords.append(v.get_coords())
        return coords

    def get_coords_str(self):
        ret = "["
        for v in self.vertices:
            ret += v.get_coords_str()
        ret += "]"
        return ret

    def central_vertex(self):
        vertex_num = len(self)
        if vertex_num > 0:
            central_vertex = int(vertex_num/2)
            return MyPoint(self.vertices[central_vertex].get_coords(), name="")
        else:
            return None

    def length(self):
        l = 0
        if len(self.vertices)>1:
            p0 = self.vertices[0]
            for p1 in self.vertices[1:]:
                l += p0.dist(p1)
                p0 = p1
        return l

    def get_info(self):
        return self.get_name() + ":\n" \
                "- Coordinates:" + self.get_coords_str() +"\n" \
                "- Number of vertices:" + str(len(self.vertices)) + "\n" \
                "- Length:" + str(self.length())