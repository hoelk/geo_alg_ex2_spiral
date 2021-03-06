__author__ = 'hoelk'

from my_line import *


def make_spiral(points):
    res = MyLine()  # a line representing the CH

    while len(points) > 0:

        points.sort(key=lambda p: p.x)  # sort points from left to right
        remaining_points = []

        if len(points) < 3:
            print(str(len(points)) + 'remaining' + str(points))
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

        if len(points) < 3:
            res.add_vertices(points)
            points = None
        else:
            us = make_half_spiral(points, upper=True)
            remaining_points = us[1]

            # Prevent duplicated vertices
            if len(res) > 0:
                res.vertices.extend(us[0].vertices[1:])
            else:
                res.vertices = us[0].vertices

            if len(us[1]) > 2:
                ls = make_half_spiral(remaining_points, upper=False)
                remaining_points = ls[1]
                res.vertices.extend(ls[0].vertices[1:]) # prevent duplicated vertices
            points = remaining_points

    return res


# build the upper hull
def make_half_spiral(points, upper=True):
    spiral_points = MyLine()
    remaining_points = []

    if upper:
        points.sort(key=lambda p: p.x)
    else:
        points.sort(key=lambda p: -p.x)

    print(points)

    if len(points) > 3:
        spiral_points.add_vertex(points[0], False)
        spiral_points.add_vertex(points[1], False)

        for p in points[2:]:
            while len(spiral_points) >= 2 and p.pt_pos(spiral_points.vertices[-2], spiral_points.vertices[-1]) != LEFT:
                    remaining_points.append(spiral_points.vertices[-1])
                    spiral_points.vertices = spiral_points.vertices[:-1]
            spiral_points.add_vertex(p, False)

        remaining_points.append(p)

    else:
        print('3 points method')
        if points[2].pt_pos(points[0], points[1]) == LEFT:
            print([points[0], points[1]])
            spiral_points.vertices = [points[0], points[1]]
            remaining_points.append(points[2])
        elif points[2].pt_pos(points[0], points[1]) != LEFT:
            print([points[0], points[2]])
            spiral_points.vertices = [points[0], points[2]]
            remaining_points.append(points[1])

    print(spiral_points)
    print(remaining_points)

    return [spiral_points, remaining_points]

#
# # build the lower hull
# def make_lower_spiral(points):
#     points.sort(key=lambda p: p.x)
#     spiral_points = MyLine()  # the lower hull
#     remaining_points = []
#     spiral_points.add_vertex(points[-1], False)
#     spiral_points.add_vertex(points[-2], False)  # second-last element
#     points = reversed(points[:-2])
#
#     for p in points:
#         while len(spiral_points) >= 2 and p.pt_pos(spiral_points.vertices[-2], spiral_points.vertices[-1]) != LEFT:
#             remaining_points.append(spiral_points.vertices[-1])
#             spiral_points.vertices = spiral_points.vertices[:-1]
#
#         spiral_points.add_vertex(p, False)
#
#     # Last point of LS is starting point of next US
#     remaining_points.append(p)
#     print(' last remaining point ' + str(p))
#
#     return [spiral_points, remaining_points]

