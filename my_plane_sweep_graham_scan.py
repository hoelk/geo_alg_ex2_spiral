__author__ = 'tremity'

from my_line import *

# NOTE: in the VO we have seen the algorithm for points distributed in a "standard" cartesian coordinate system
# however, the canvas uses a non-standard cartesian system where the y-axis is flipped.
# We have to take into account this in the code (that is why it is slightly different
# from the pseudo-code seen in class)
# This function realize the graham algorithm in a way that is graphically identical to the version seen in class
# That is, we select the bottom-left-most point of the set and build the convex hull in counterclockwise order
# Below there is another version that follow the pseudo-code seen in class more precisely, but, graphically, correspond
# to a y-flipped realization
def convex_hull_graham_plain(point_list):
    the_ch = MyLine()  # this will be the convex hull of point_list

    if len(point_list) < 4:
        the_ch.add_vertices(point_list, False)
    else:
        # sort the point list from left to right
        point_list.sort(key=lambda p: p.x)
        # sort the point list from bottom to top, graphically. But from top to bottom coordinate-wise
        point_list.sort(key=lambda p: p.y, reverse=True)

        # select the bottom-left-most point as the pivot (and remove it from the list)
        pivot = point_list.pop(0)

        # sort remaining point by
        # 1) their distance from pivot
        point_list.sort(key=lambda p: pivot.dist(p))
        # 2) their polar angle wrt pivot in counterclockwise order around pivot
        point_list.sort(key=lambda p: atan2(p.y - pivot.y, p.x - pivot.x), reverse=True)

        # add the pivot to the CH
        the_ch.add_vertex(pivot, False)

        # for the rest of the points...
        # until when the last turn formed by
        # 1) the second last element of the CH
        # 2) the last element of the CH
        # 3) the point under consideration
        # is a non-right turn, pop the last element from the list
        for p in point_list:
            while len(the_ch) >= 2 and p.pt_pos(the_ch.vertices[-2], the_ch.vertices[-1]) != RIGHT:
                the_ch.vertices.pop()
            the_ch.add_vertex(p, False)

        # finally, let us close the line
        the_ch.add_vertex(pivot, False)

    return the_ch


# This version of the graham scan follows accurately the pseudo-code seen in class but, graphically, it is flipped
# along the y dimension:
# the pivot is the top-left-most
def convex_hull_graham_plain_y_flipped(point_list):
    the_ch = MyLine()  # a line representing the CH

    if len(point_list) < 4:
        the_ch.add_vertices(point_list, False)
    else:
        # sort the point list from left to right
        point_list.sort(key=lambda p: p.x)
        # sort the point list from top to bottom (graphically). but bottom to top coordinate-wise
        point_list.sort(key=lambda p: p.y)

        # select the top-left-most point as the pivot (and remove it from the list)
        pivot = point_list.pop(0)

        # sort remaining point by
        # 1) their distance from pivot
        point_list.sort(key=lambda p: pivot.dist(p))
        # 2) their polar angle wrt pivot in counterclockwise order around pivot
        # This can introduce rounding errors -> nicer solution, look at 'precise' version
        point_list.sort(key=lambda p: atan2(p.y - pivot.y, p.x - pivot.x))

        # add the pivot to the CH
        the_ch.add_vertex(pivot, False)

        # for the rest of the points...
        # until when the last turn formed by
        # 1) the second last element of the CH
        # 2) the last element of the CH
        # 3) the point under consideration
        # is a non-left turn, pop the last element from the list
        for p in point_list:
            while len(the_ch) >= 2 and p.pt_pos(the_ch.vertices[-2], the_ch.vertices[-1]) != LEFT:
                the_ch.vertices = the_ch.vertices[:-1]
            the_ch.add_vertex(p, False)

        # finally, let us close the line
        the_ch.add_vertex(pivot, False)

    return the_ch


# this is an implementation of the graham scan (higher precision variant) seen in class
# It does not resort to the arctan function which can introduce rounding errors
def convex_hull_graham_precise(point_list):
    the_ch = MyLine()  # a line representing the CH

    if len(point_list) < 4:
        the_ch.add_vertices(point_list, False)
    else:
        point_list.sort(key=lambda p: p.x)  # sort points from left to right
        the_uh = upper_hull(point_list)  # upper hull
        the_lh = lower_hull(point_list)  # lower hull


        # Extend appends the elements from an iterable
        # append appends the whole object
        # example [1, 2, 3].append [5, 6] --> [1, 2, 3, [4, 5]]
        the_ch.vertices.extend(the_uh.vertices)
        the_ch.vertices.extend(the_lh.vertices[1:])

        upper_text = "UH=["
        for p in the_uh.vertices:
            upper_text += p.get_name() + ", "
        upper_text += "]"

        lower_text = "UH=["
        for p in the_lh.vertices:
            lower_text += p.get_name() + ", "
        lower_text += "]"

        print(upper_text)
        print(lower_text)


    return the_ch


# build the upper hull
def upper_hull(point_list):
    the_uh = MyLine()  # the upper hull
    the_uh.add_vertex(point_list[0], False)
    the_uh.add_vertex(point_list[1], False)

    for p in point_list[2:]:
        while len(the_uh) >= 2 and p.pt_pos(the_uh.vertices[-2], the_uh.vertices[-1]) != LEFT:
            the_uh.vertices = the_uh.vertices[:-1]
        the_uh.add_vertex(p, False)

    return the_uh

# build the lower hull
def lower_hull(point_list):
    the_lh = MyLine()  # the lower hull
    the_lh.add_vertex(point_list[-1], False)  #last element
    the_lh.add_vertex(point_list[-2], False)  #second-last element

    for p in reversed(point_list[:-2]):
        while len(the_lh) >= 2 and p.pt_pos(the_lh.vertices[-2], the_lh.vertices[-1]) != LEFT:
            the_lh.vertices = the_lh.vertices[:-1]
        the_lh.add_vertex(p, False)

    return the_lh



