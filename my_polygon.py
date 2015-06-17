__author__ = 'tremity'

from my_segment import *
from my_shape import *


class MyPolygon(MyShape):
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
            MyPolygon.last_auto_name += 1
            kwargs['name'] = 'P'+str(MyPolygon.last_auto_name)
        super().__init__(*args, **kwargs)

        #print("Created polygon with id: " + str(self.id))
        MyPolygon.counter += 1

    def __del__(self):
        MyPolygon.counter -= 1
        #print("Destroying polygon with id: " + str(self.id))

    def __str__(self):
        return self.get_name() + self.get_coords_str()

    def __len__(self):
        return len(self.vertices)

    def add_vertices(self, vs):
        for v in vs:
            if len(v) == 2 and all(any(isinstance(coord, num_type) for num_type in (int, float)) for coord in v):
                #print(str(v))
                self.add_vertex(MyPoint(v[0], v[1], name=""))

    def add_vertex(self, p):
        if not isinstance(p, MyPoint):
            p = MyPoint(p, name="")  # create and anonymous point

        if isinstance(p, MyPoint):
            if p.name and p.name != "":  # if it is not an anonymous point
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

    def centroid(self):
        x = y = 0
        for p in self.vertices:
            x += p.x
            y += p.y

        return MyPoint(x/len(self), y/len(self), name="")

    def perimeter(self):
        l = 0
        if len(self.vertices) > 1:
            p0 = self.vertices[0]
            for p1 in self.vertices[1:]:
                l += p0.dist(p1)
                p0 = p1
        return l

    def get_info(self):
        return self.get_name() + ":\n" \
                "- Coordinates:" + self.get_coords_str() + "\n" \
                "- Number of vertices:" + str(len(self.vertices)) + "\n" \
                "- Perimeter:" + str(self.perimeter()) + "\n" \
                "- Centroid:" +str(self.centroid())

    def is_point_on_boundary(self, p):
        if isinstance(p, MyPoint):
            for i in range(len(self)):
                curr_edge = MySegment(vertices=[self.vertices[i], self.vertices[(i+1) % len(self)]], name="")
                if p.pt_pos(self.vertices[i], self.vertices[(i+1) % len(self)]) == BETWEEN:
                    return True
            return False
        return None

    def is_point_in(self, p):
        if isinstance(p, MyPoint):
            if self.is_point_on_boundary(p):  # we decide that the boundary is not part of the interior of the polygon!
                return False

            is_in = False
            ray = MySegment(vertices=[p, p], name="")

            for i in range(len(self)):
                curr_edge = MySegment(vertices=[self.vertices[i], self.vertices[(i+1) % len(self)]], name="")
                x_max = max(curr_edge.vertices[0].x, curr_edge.vertices[1].x)
                if x_max >= p.x:
                    ray.vertices[1].x = x_max+1
                    if ray.intersects(curr_edge):
                        is_in = not is_in

            return is_in
        return None


# poly = MyPolygon(vertices=[(0,0), (5,1), (3,1), (5,2), (3,5), (3,2)])
# p = MyPoint(3, -1.5)
#
# print(str(poly.is_point_in(p)))