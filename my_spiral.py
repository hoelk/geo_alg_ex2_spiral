__author__ = 'hoelk'

from my_line import *


def make_spiral(points):
    res = MyLine()  # a line representing the CH

    while len(points) > 0:

        points.sort(key=lambda p: p.x)  # sort points from left to right
        remaining_points = []

        if len(points) < 4:
            res.add_vertices(points, False)
            points = []
        else:
            # Sort points from left to right and top to bottom
            points.sort(key=lambda p: p.x)
            points.sort(key=lambda p: p.y)

            # select the top-left-most point as the pivot (and remove it from the list)
            pivot = points.pop(0)

            # sort remaining point by distance from pivot and polar angle wrt (ccw)
            points.sort(key=lambda p: pivot.dist(p))
            points.sort(key=lambda p: atan2(p.y - pivot.y, p.x - pivot.x))

            # add the pivot to the CH
            res.add_vertex(pivot, False)

            # for the rest of the points...
            # until when the last turn formed by
            # 1) the second last element of the CH
            # 2) the last element of the CH
            # 3) the point under consideration
            # is a non-left turn, pop the last element from the list
            for p in points:
                while len(res) >= 2 and p.pt_pos(res.vertices[-2], res.vertices[-1]) != LEFT:
                    remaining_points.append(res.vertices[-1])
                    res.vertices = res.vertices[:-1]
                res.add_vertex(p, False)

            # finally, let us close the line

            points = remaining_points


            # res.add_vertex(pivot, False)

    return res


def make_spiral_precise(points):
    res = MyLine()  # a line representing the CH
    upper_spiral = MyLine()
    lower_spiral = MyLine()

    points.sort(key=lambda p: p.x)
    while isinstance(points, list):

        if len(points) == 1:
            res.add_vertex(points)
        if len(points) == 2:
            print('<3 remaining : ' + str(points))

            if points[0] not in res.vertices and points[1] not in res.vertices:
                res.add_vertices(points, False)
            elif points[0] not in res.vertices:
                res.add_vertex(points[0])
            else:
                res.add_vertex(points[1])
            points = None
        else:
            us = make_upper_spiral(points)
            upper_spiral = us[0]
            remaining_points = us[1]

            # Prevent duplicated vertices
            if len(res) > 0:
                res.vertices.extend(us[0].vertices[1:])
            else:
                res.vertices.extend(us[0].vertices)

            if len(us[1]) > 3:
                ls = make_lower_spiral(remaining_points)
                remaining_points = ls[1]
                res.vertices.extend(ls[0].vertices[1:]) # prevent duplicated vertices

            points = remaining_points


    upper_text = "US=["
    for p in upper_spiral.vertices:
        upper_text += p.get_name() + ", "
    upper_text += "]"

    lower_text = "US=["
    for p in lower_spiral.vertices:
        lower_text += p.get_name() + ", "
    lower_text += "]"

    return res


# build the upper hull
def make_upper_spiral(points):
    points.sort(key=lambda p: p.x)
    spiral_points = MyLine()
    remaining_points = []

    spiral_points.add_vertex(points[0], False)
    spiral_points.add_vertex(points[1], False)

    for p in points[2:]:
        while len(spiral_points) >= 2 and p.pt_pos(spiral_points.vertices[-2], spiral_points.vertices[-1]) != LEFT:
            remaining_points.append(spiral_points.vertices[-1])
            spiral_points.vertices = spiral_points.vertices[:-1]

        spiral_points.add_vertex(p, False)

    remaining_points.append(p)
    return [spiral_points, remaining_points]


# build the lower hull
def make_lower_spiral(points):
    points.sort(key=lambda p: p.x)
    spiral_points = MyLine()  # the lower hull
    remaining_points = []
    spiral_points.add_vertex(points[-1], False)
    spiral_points.add_vertex(points[-2], False)  # second-last element
    points = reversed(points[:-2])

    for p in points:
        while len(spiral_points) >= 2 and p.pt_pos(spiral_points.vertices[-2], spiral_points.vertices[-1]) != LEFT:
            remaining_points.append(spiral_points.vertices[-1])
            spiral_points.vertices = spiral_points.vertices[:-1]

        spiral_points.add_vertex(p, False)

    # Last point of LS is starting point of nex US
    remaining_points.append(p)

    return [spiral_points, remaining_points]

