__author__ = 'tremity'

from my_line import *


class MySegment(MyLine):
    counter = 0
    last_auto_name = 0

    def __init__(self, *args, **kwargs):
        if "name" not in kwargs:
            MySegment.last_auto_name += 1
            kwargs['name'] = 'S'+str(MySegment.last_auto_name)
        super().__init__(*args, **kwargs)

        if len(self.vertices) > 2:
            self.vertices = self.vertices[:2]

        MySegment.counter += 1

    def __del__(self):
        MySegment.counter -= 1
        #print("Destroyed segmane with id: " + str(self.id))

    def add_vertex(self, p):
        if not isinstance(p, MyPoint):
            p = MyPoint(p, name="")  # create and anonymous point

        if p.name and p.name != "":  # if it is not an anonymous point
            p = MyPoint(p.x, p.y, name="")  # create a copy that is anonymous

        if len(self) < 2:  # a segment cannot have more than 2 vertices
            self.vertices.append(p)
        else:
            self.vertices[1] = p

    def get_info(self):
        return self.get_name() + ":\n" \
                "- Coordinates:" + self.get_coords_str() +"\n" \
                "- Length:" + str(self.length())

    def is_collinear(self, s):
        if isinstance(s, MySegment):
            if s.vertices[0].pt_pos(self.vertices[0], self.vertices[1]) in (BEFORE, BETWEEN, AFTER) and \
               s.vertices[1].pt_pos(self.vertices[0], self.vertices[1]) in (BEFORE, BETWEEN, AFTER):
                return True
            return False

        return None

    def intersects(self, s):

        if isinstance(s, MySegment):
            s0_pos = s.vertices[0].pt_pos(self.vertices[0], self.vertices[1])  #position of s.vertices[0] wrt self.vertices[0],self.vertices[1]
            s1_pos = s.vertices[1].pt_pos(self.vertices[0], self.vertices[1])  #position of s.vertices[1] wrt self.vertices[0],self.vertices[1]
            self0_pos = self.vertices[0].pt_pos(s.vertices[0], s.vertices[1])  #position of self.vertices[0] wrt s.vertices[0],s.vertices[1]
            self1_pos = self.vertices[1].pt_pos(s.vertices[0], s.vertices[1])  #position of self.vertices[0] wrt s.vertices[0],s.vertices[1]

            # General case: non-collinear segments
            if s0_pos != s1_pos and self0_pos != self1_pos:
                return True

            # Special Cases: segments are collinear (so, obviously the previous if can never be verified)
            if s0_pos == BETWEEN and s1_pos == BETWEEN:
                return True
            if self0_pos == BETWEEN and self1_pos == BETWEEN:
                return True

            return False

        return None

    def segment_intersection(self, other):
        #self= [p,p+r]; other=[q,q+other]
        if isinstance(other, MySegment):  # if other is actually a segment
            if self.intersects(other):  # if the segments intersect
                #print("INTERSECT")
                if not self.is_collinear(other): # general case
                    #print("NOT COLLINEAR")
                    p = self.vertices[0]
                    q = other.vertices[0]
                    r = self.vertices[1] - self.vertices[0]
                    s = other.vertices[1] - other.vertices[0]

                    t = (q - p).cross_product(s) / r.cross_product(s)

                    return MyPoint(p.x + t*r.x, p.y + t*r.y, name=self.get_name()+"x"+other.get_name())
                else:  # special case: collinear segments
                    #print("COLLINEAR")
                    s0_pos = other.vertices[0].pt_pos(self.vertices[0], self.vertices[1])  #position of other.vertices[0] wrt self.vertices[0],self.vertices[1]
                    s1_pos = other.vertices[1].pt_pos(self.vertices[0], self.vertices[1])  #position of other.vertices[1] wrt self.vertices[0],self.vertices[1]

                    start = None
                    end = None

                    if s0_pos == BEFORE or s1_pos == BEFORE:  # if one vertex of other is before self
                        #print("ONE VERTEX OF S IS BEFORE")
                        start = self.vertices[0]  # the resulting segment starts at self[0]
                        if s0_pos == BETWEEN:
                            #print("S[0] IS BETWEEN")
                            end = other.vertices[0]
                        elif s1_pos == BETWEEN:
                            #print("S[1] IS BETWEEN")
                            end = other.vertices[1]
                        elif s0_pos == AFTER or s1_pos == AFTER:
                            #print("THE OTHER VERTEX IS AFTER")
                            end = self.vertices[1]
                    else:  # at least one vertex of other must lie between self[0] and self[1] (because we know they intersect and are collinear)
                        #print("ONE VERTEX OF S IS BETWEEN")
                        # assume other is completely inside self
                        start = other.vertices[0]  # then the intersection coincides with other
                        end = other.vertices[1]

                        if s0_pos == AFTER:
                            start = self.vertices[1]  # the intersection starts at self[1]
                        elif s1_pos == AFTER:
                            end = self.vertices[1]  # the intersection ends at self[1]

                    #print("start:"+str(start))
                    #print("end:"+str(end))
                    if start != end:

                        return MySegment(vertices=[start, end], name=self.get_name()+"x"+other.get_name())
                    else:
                        return MyPoint(start.x, start.y, name=self.get_name()+"x"+other.get_name())

        return None



# ls = []
# ls.append(MySegment(vertices=[[-1, -1], [1, 0]]))
# ls.append(MySegment(vertices=[[-1, 1], [0, 0]]))
# ls.append(MySegment(vertices=[[-1, 2], [1, -1]]))
#
# ls.append(MySegment(vertices=[[5, 0], [10, 0]]))
# ls.append(MySegment(vertices=[[0, 0], [4, 0]]))
# ls.append(MySegment(vertices=[[0, 0], [6, 0]]))
# ls.append(MySegment(vertices=[[6, 0], [9, 0]]))
# ls.append(MySegment(vertices=[[7, 0], [10, 0]]))
#
# for i in range(len(ls)):
#     for j in range(i+1, len(ls)):
#         print(str(ls[i]) + ", " + str(ls[j]) + ":" + str(ls[i].segment_intersection(ls[j])))
#         print(str(ls[j]) + ", " + str(ls[i]) + ":" + str(ls[j].segment_intersection(ls[i])))

