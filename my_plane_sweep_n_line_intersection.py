__author__ = 'tremity'

#WORKS ONLY FOR GENERAL POSITION:
# no lines parallel to x-axis
# no three lines intersect in the same point
# intersection points do not coincide with segment extremes
# segments extremes do not coincide

from my_segment import *

EVENT_UPPER = 0
EVENT_LOWER = 1
EVENT_INTERSECT = 2

SWEEP = MySegment(vertices=[[0, 0], [0, 0]], name="SWEEP LINE")

class Event():
    def __init__(self, point, segments, type):
        self.point = point

        self.segments = segments
        # a list of segments to which self.point belongs
        # this list can contain either 1 or 2 segments
        # if 2 segments they must be listed from left to right
        # as they intersect the sweep line at current position

        self.type = type

    def __str__(self):
        segs = ""
        for s in self.segments:
            segs += s.get_name()
        return "point:" + str(self.point) + "[" + segs + "]"

    def __repr__(self):
        return str(self)

def sort_Q(Q):
    Q.sort(key=lambda e: e.point.x)
    Q.sort(key=lambda e: e.point.y, reverse=True)

def sort_along_sweep(s):
    intersection = SWEEP.segment_intersection(s)
    if isinstance(intersection, MySegment):
        return min(intersection.vertices[0].x, intersection.vertices[1].x)
    #if it is not a segment, it must be a point (because of how we move the sweep line)
    return intersection.x

def find_right_neighbour(S, segment):
    i = S.index(segment)
    rn = None
    if i < (len(S)-1):
        rn = S[i+1]
    return rn

def find_left_neighbour(S, segment):
    i = S.index(segment)
    ln = None
    if i > 0:
        ln = S[i-1]
    return ln

def find_new_event(ls, rs, Q, O, curr_pos):
    if ls and rs:
        intersection_point = ls.segment_intersection(rs)
        if intersection_point and isinstance(intersection_point, MyPoint) and \
                (intersection_point.y < curr_pos.y or
                     (intersection_point.y == curr_pos.y and intersection_point.y > curr_pos.x)):
            Q.append(Event(intersection_point, [ls, rs], EVENT_INTERSECT))
            sort_Q(Q)
            O.append(intersection_point)

def handle_event(Q, S, O):
    e = Q.pop(0)  # take first event in the queue
    SWEEP.vertices[0].y = SWEEP.vertices[1].y = e.point.y  # lower the sweep line

    if e.type == EVENT_UPPER:
        s = e.segments[0]
        S.append(s)
        S.sort(key=sort_along_sweep)
        ln, rn = find_left_neighbour(S, s), find_right_neighbour(S, s)

        find_new_event(ln, s, Q, O, e.point)
        find_new_event(s, rn, Q, O, e.point)

    elif e.type == EVENT_LOWER:
        s = e.segments[0]
        ln, rn = find_left_neighbour(S, s), find_right_neighbour(S, s)

        S.remove(s)
        S.sort(key=sort_along_sweep)

        find_new_event(ln, rn, Q, O, e.point)

    else:
        ls, rs = e.segments
        ln, rn = find_left_neighbour(S, ls), find_right_neighbour(S, rs)
        li = S.index(ls)
        ri = S.index(rs)
        S[li], S[ri] = rs, ls # swap ls and rs in the state

        find_new_event(ls, rn, Q, O, e.point)
        find_new_event(ln, rs, Q, O, e.point)


def n_line_intersection(segment_list):
    O = []  # the output will be a list of intersection points
    Q = []  # the event queue
    S = []  # the state of the sweep line

    for s in segment_list:
        upper = s.vertices[0]
        lower = s.vertices[1]
        if upper.y < lower.y or (upper.y == lower.y and upper.x > lower.x):
            upper = s.vertices[1]
            lower = s.vertices[0]
        Q.append(Event(upper, [s], EVENT_UPPER))  # extract first extreme of the segment
        Q.append(Event(lower, [s], EVENT_LOWER))  # extract second extreme of the segment

        for v in s.vertices:
            # extend and "raise" the sweep line
            if SWEEP.vertices[0].y < v.y:
                SWEEP.vertices[0].y = SWEEP.vertices[1].y = v.y
            if SWEEP.vertices[0].x > v.x:
                SWEEP.vertices[0].x = v.x
            if SWEEP.vertices[1].x < v.x:
                SWEEP.vertices[1].x = v.x
    #print(str(Q))
    sort_Q(Q)
    #print(str(Q))
    SWEEP.vertices[0].x -= 1  # make sure the sweep line is long enough to check for intersection with every segment
    SWEEP.vertices[1].x += 1

    while len(Q) > 0:
        handle_event(Q, S, O)

    return O


# segs = []
#
# s1 = MySegment(vertices=[[0, -1], [0, 1]])
# s2 = MySegment(vertices=[[0.5, 1.5], [2, 1]])
# s3 = MySegment(vertices=[[-1, -1], [3, 3]])
# s4 = MySegment(vertices=[[2, 1.5], [1, 0.5]])
#
# segs.append(s2)
# segs.append(s4)
# segs.append(s1)
# segs.append(s3)
#
# o = n_line_intersection(segs)

#print(str(o))
