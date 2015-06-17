__author__ = 'tremity'


VERSION = '0.5.3'  # version of the drawing app

ZOOM_IN = 1.1  # zoom-in scale
ZOOM_OUT = 1/ZOOM_IN  # zoom-out scale(must be the inverse of zoom-in, otherwise we cannot come back to original zoom)

TOOL_ERASE = 0
TOOL_DRAW = 1
TOOL_INFO = 2
TOOL_OPERATION = 3

# the following constants define operations
OPERATION_POINT_IN_POLY = "Point in polygon"
OPERATION_SEGMENT_INTERSECT = "Segments intersect"
OPERATION_SEGMENT_INTERSECTION = "Segments intersection"
OPERATION_N_SEGMENT_INTERSECTION = "N-Segments intersection"
OPERATION_CONVEX_HULL_GRAHAM_PLAIN = "Convex Hull (graham-plain)"
OPERATION_CONVEX_HULL_GRAHAM_PRECISE = "Convex Hull (graham-precise)"
OPERATION_SPIRAL = "Spiral"
OPERATION_SPIRAL_PRECISE = "Spiral (precise)"

# DO NOT FORGET to add the operation constants to this list in order to have it displayed in
# the drop-down menu in the drawing application
OPERATIONS = [OPERATION_POINT_IN_POLY,
              OPERATION_SEGMENT_INTERSECT,
              OPERATION_SEGMENT_INTERSECTION,
              OPERATION_N_SEGMENT_INTERSECTION,
              OPERATION_CONVEX_HULL_GRAHAM_PLAIN,
              OPERATION_CONVEX_HULL_GRAHAM_PRECISE,
              OPERATION_SPIRAL,
              OPERATION_SPIRAL_PRECISE]

POINT = 1
LINE = 2
POLYGON = 3
SEGMENT = 4
TRIANGLE = 5

POINT_RADIUS = 4  # points are drawn as circles, this is the radius
VERTEX_RADIUS = 4  # vertices of non-finished lines and polygons are drawn as Xs, this is the "radius"

STATUS = {
    TOOL_DRAW:{
        POINT: "Drawing points",
        LINE: "Drawing lines",
        POLYGON: "Drawing polygons",
        SEGMENT: "Drawing segments",
        TRIANGLE: "Drawing triangles"
    },
    TOOL_ERASE: "Erasing shapes",
    TOOL_INFO: "Selecting shapes",
    TOOL_OPERATION: "Perform an operation"

}

INFO = {
    TOOL_DRAW: {
        POINT:      "Left-click anywhere on the canvas to set a point.",
        LINE:       "Left-click anywhere on the canvas to set a vertex "
                    "OR move the mouse while holding down the left button "
                    "to move the vertex accordingly and release the button "
                    "to set the vertex. "
                    "\nPress ENTER when the line is complete."
                    "\nPress ESCAPE to stop drawing the line."
                    "\nPress BACKSPACE to delete last drawn vertex.",
        POLYGON:    "Left-click anywhere on the canvas to set a vertex "
                    "OR move the mouse while holding down the left button "
                    "to move the vertex accordingly and release the button "
                    "to set the vertex. "
                    "\nPress ENTER when the polygon is complete."
                    "\nPress ESCAPE to stop drawing the polygon."
                    "\nPress BACKSPACE to delete last drawn vertex.",
        SEGMENT:    "Draw two points",
        TRIANGLE:   "Draw three points"
        },
    TOOL_ERASE:     "Draw a selection box by pressing the left button of the mouse "
                    "and dragging the mouse. Every shape falling inside the area "
                    "or overlapping it will be erased.",
    TOOL_INFO:     "Draw a selection box by pressing the left button of the mouse "
                    "and dragging the mouse. Information about each shape falling inside the area "
                    "or overlapping it will be shown in the shape info box.",
    TOOL_OPERATION: "Select an operation to perform from the drop-down menu, select a series of shapes "
                    "from the canvas and click the button to start the operation."
    }

SHAPE_INFO_WINDOW_WIDTH = 350
SHAPE_INFO_WINDOW_HEIGHT = 500

RIGHT = "RIGHT"
LEFT = "LEFT"
COLLINEAR = "COLLINEAR"
BETWEEN = "BETWEEN"
BEFORE = "BEFORE"
AFTER = "AFTER"



