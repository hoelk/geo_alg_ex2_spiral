__author__ = 'tremity'

from my_polygon import *


class MyTriangle(MyPolygon):
    counter = 0
    last_auto_name = 0

    def __init__(self, *args, **kwargs):
        if "name" not in kwargs:
            MyTriangle.last_auto_name += 1
            kwargs['name'] = 'T'+str(MyTriangle.last_auto_name)
        super().__init__(*args, **kwargs)

        if len(self.vertices) > 3:
            self.vertices = self.vertices[:3]

        MyTriangle.counter += 1

    def __del__(self):
        MyTriangle.counter -= 1
        #print("Destroyed triangle with id: " + str(self.id))

    def add_vertex(self, p):
        if not isinstance(p, MyPoint):
            p = MyPoint(p, name="")  # create and anonymous point

        if p.name and p.name != "":  # if it is not an anonymous point
            p = MyPoint(p.x, p.y, name="")  # create a copy that is anonymous

        if len(self) < 3:  # a triangle cannot have more than 3 vertices
            self.vertices.append(p)
        else:
            self.vertices[2] = p

    def get_area(self):
        return "TO-DO"

    def get_angles_amplitude(self):
        return "TO-DO"

    def get_incenter(self):
        return "TO-DO"

    def get_circumcenter(self):
        return "TO-DO"

    def get_orthocenter(self):
        return "TO-DO"

    def get_type_edge(self):
        return "TO-DO"

    def get_type_angle(self):
        return "TO-DO"

    def get_info(self):
        return self.get_name() + ":\n" \
                "- Coordinates:" + self.get_coords_str() +"\n" \
                "- Perimeter:" + str(self.perimeter()) + "\n" \
                "- Area:" +str(self.get_area()) + "\n" \
                "- Centroid:" +str(self.centroid()) + "\n" \
                "- Amplitude of angles:" +str(self.get_angles_amplitude()) + "\n" \
                "- Incenter:" +str(self.get_incenter()) + "\n" \
                "- Circumcenter:" +str(self.get_circumcenter()) + "\n" \
                "- Orthocenter:" +str(self.get_orthocenter()) + "\n" \
                "- Type(Edges):" +str(self.get_type_edge()) + "\n" \
                "- Type(Angles):" +str(self.get_type_angle()) + "\n"