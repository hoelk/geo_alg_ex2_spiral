__author__ = 'tremity'

import tkinter as tk
from my_triangle import *
from my_rectangle import *
from my_segment import *
from my_constants import *
from tk_infobox import *
from my_plane_sweep_n_line_intersection import *
from my_plane_sweep_graham_scan import *
from my_spiral import *


class MyDrawingApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.points = {}  # list of all drawn points
        self.lines = {}  # list of all drawn lines
        self.polygons = {}  # list of all drawn polygons
        self.segments = {}  # list of all drawn segments
        self.triangles = {}  # list of all drawn triangles

        self.shape_id_to_canvas_id = {}  # key=shape_id, value=canvas_id for the shape (used to manage the drawing)
        self.canvas_id_to_shape_id = {}  # key=canvas_id, value=shape_id
        self.shape_id_to_canvas_text_id = {}  # key=shape_id, value=canvas_id for the text associated to the shape
        self.selected_canvas_shape_ids = []

        self.curr_shape = None  # here we keep the shape being drawn until it is finished, then we draw it on canvas
                                # and store it in the opportune data structures (lists and dictionaries, see above)
        self.curr_tool = None  # the tool currently selected
        self.curr_shape_type = None  # type of shape currently being drawn (if any)
        self.selection_box = None  # a rectangle to select shapes on canvas
        self.canvas = None  # used to draw

        self.tool_group = tk.IntVar()  # used to group radiobuttons for the tool selection
        self.statusbar_text = tk.StringVar()  # text in the status bar
        self.operation_var = tk.StringVar()  # which operation is selected
        self.info_box_text = tk.StringVar()  # text in the info box
        self.shape_info_box_text = tk.StringVar()  # text in the shape info box
        self.operation_info_box_text = tk.StringVar()  # text in the operation info box

        self._init_canvas()  # initialize the canvas
        self._init_right_sidebar()  # initialize the sidebar
        self._init_statusbar()  # initialize the statusbar

        self.update()  # here the window is fully built. this function updates all window attributes
        self.minsize(self.winfo_width(), self.winfo_height())  # now we can enforce a minimal size for the window

        self.geometry('%dx%d+%d+%d' % (self.winfo_width(), self.winfo_height(), 0, 0))
        #place the main window at the top-left corner of screen

        self.change_tool(TOOL_DRAW, POINT)  # let us choose a tool

    def _init_canvas(self):
        self.canvas = tk.Canvas(self, width=400, height=400, cursor="cross")
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)  # place the canvas at (row,column) (0,0)
        self.columnconfigure(0, weight=1)  # expand the column when the window is resized
        self.rowconfigure(0, weight=1)  # expand the row when the window is resized

        self.canvas.bind("<ButtonPress-1>", self.on_left_btn_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_btn_release)
        self.canvas.bind("<B1-Motion>", self.on_left_btn_move)
        self.bind("<Key>", self.on_key_press)

    def _init_right_sidebar(self):
        #----------------------------------------
        # vertical separator (no native way for this, so we should use a trick: a 1px-width black frame)
        #----------------------------------------
        tk.Frame(self, width=1, bg="black").grid(row=0, column=1, sticky=tk.N+tk.S)

        # frame (a container) for the right sidebar
        frame_right_sidebar = tk.Frame(self, width=250)  # a frame under which we place other items
        frame_right_sidebar.grid(row=0, column=2, sticky=tk.N)
        self.columnconfigure(2, minsize=250)  # this assures that the column of the main window where the
                                              # sidebar is positioned does not get smaller than 250px

        #----------------------------------------
        # a frame for the tools
        #----------------------------------------
        frame_tools = tk.Frame(frame_right_sidebar)
        frame_tools.grid(row=0, column=0, sticky=tk.W+tk.E)

        #title for the tools
        title_tools = tk.Label(frame_tools, text="Tools", anchor=tk.W)  # a title
        title_tools.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E+tk.S)  # place the title in the frame

        #radio buttons for the tools
        draw_point_butt = tk.Radiobutton(frame_tools, text="Draw Points",
                                         indicatoron=0, variable=self.tool_group, value=0,
                                         command=lambda: self.change_tool(new_tool=TOOL_DRAW, new_shape=POINT))
        draw_line_butt = tk.Radiobutton(frame_tools, text="Draw Lines",
                                        indicatoron=0, variable=self.tool_group, value=1,
                                        command=lambda: self.change_tool(new_tool=TOOL_DRAW, new_shape=LINE))
        draw_polygon_butt = tk.Radiobutton(frame_tools, text="Draw Polygons",
                                           indicatoron=0, variable=self.tool_group, value=2,
                                           command=lambda: self.change_tool(new_tool=TOOL_DRAW, new_shape=POLYGON))
        draw_segment_butt = tk.Radiobutton(frame_tools, text="Draw Segment",
                                           indicatoron=0, variable=self.tool_group, value=3,
                                           command=lambda: self.change_tool(new_tool=TOOL_DRAW, new_shape=SEGMENT))
        draw_triangle_butt = tk.Radiobutton(frame_tools, text="Draw Triangle",
                                           indicatoron=0, variable=self.tool_group, value=4,
                                           command=lambda: self.change_tool(new_tool=TOOL_DRAW, new_shape=TRIANGLE))
        erase_butt = tk.Radiobutton(frame_tools, text="Erase Shapes",
                                    indicatoron=0, variable=self.tool_group, value=5,
                                    command=lambda: self.change_tool(new_tool=TOOL_ERASE))
        info_butt = tk.Radiobutton(frame_tools, text="Shape Info",
                                    indicatoron=0, variable=self.tool_group, value=6,
                                    command=lambda: self.change_tool(new_tool=TOOL_INFO))
        function_butt = tk.Radiobutton(frame_tools, text="Operation",
                                    indicatoron=0, variable=self.tool_group, value=7,
                                    command=lambda: self.change_tool(new_tool=TOOL_OPERATION))

        self.operation_var.set(OPERATIONS[0])
        function_list = tk.OptionMenu(frame_tools, self.operation_var, *OPERATIONS)

        start_func_butt = tk.Button(frame_tools, text="GO", command=lambda: self.perform_operation())


        # place the buttons in the frame
        draw_point_butt.grid(row=1, column=0, sticky=tk.W)
        draw_polygon_butt.grid(row=2, column=0, sticky=tk.W)
        draw_triangle_butt.grid(row=2, column=1, sticky=tk.W)
        draw_line_butt.grid(row=3, column=0, sticky=tk.W)
        draw_segment_butt.grid(row=3, column=1, sticky=tk.W)
        erase_butt.grid(row=4, column=0, sticky=tk.W)
        info_butt.grid(row=4, column=1, sticky=tk.W)
        function_butt.grid(row=5, column=0, sticky=tk.W)
        start_func_butt.grid(row=5, column=1, sticky=tk.W)
        function_list.grid(row=6, column=0, columnspan=2, sticky=tk.W)



        #----------------------------------------
        # a separator (there seems to be no native way for this, so we should use a trick: a 1px-height black frame)
        #----------------------------------------
        tk.Frame(frame_right_sidebar, height=1, bg="black").grid(row=1, column=0, sticky=tk.N+tk.W+tk.E)

        #----------------------------------------
        #set tool info box
        #----------------------------------------
        frame_tool_info = Frame(frame_right_sidebar)
        frame_tool_info.grid(row=2, column=0, sticky=tk.N+tk.W+tk.E)
        title_tool_info = tk.Label(frame_tool_info, text="Tool Info", anchor=tk.W)  # a title
        title_tool_info.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)

        info_box_tool = InfoBox(frame_tool_info, text=self.info_box_text, width=250, height=100)
        info_box_tool.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W+tk.E)  # place the frame in the right sidebar
        frame_right_sidebar.columnconfigure(2, weight=1)
        frame_right_sidebar.rowconfigure(1, weight=1)

        #----------------------------------------
        # a separator (there seems to be no native way for this, so we should use a trick: a 1px-height black frame)
        #----------------------------------------
        tk.Frame(frame_right_sidebar, height=1, bg="black").grid(row=3, column=0, sticky=tk.N+tk.W+tk.E)

        #----------------------------------------
        #set shape info box
        #----------------------------------------
        frame_shape_info = Frame(frame_right_sidebar)
        frame_shape_info.grid(row=4, column=0, sticky=tk.N+tk.W+tk.E)
        title_shape_info = tk.Label(frame_shape_info, text="Shape Info", anchor=tk.W)  # a title
        title_shape_info.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)

        info_box_shape = InfoBox(frame_shape_info, text=self.shape_info_box_text, width=250, height=100)
        info_box_shape.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W+tk.E)  # place the frame in the right sidebar
        frame_right_sidebar.rowconfigure(4, weight=1)

        #----------------------------------------
        # a separator (there seems to be no native way for this, so we should use a trick: a 1px-height black frame)
        #----------------------------------------
        tk.Frame(frame_right_sidebar, height=1, bg="black").grid(row=5, column=0, sticky=tk.N+tk.W+tk.E)

        #----------------------------------------
        #set shape info box
        #----------------------------------------
        frame_operation_info = Frame(frame_right_sidebar)
        frame_operation_info.grid(row=6, column=0, sticky=tk.N+tk.W+tk.E)
        title_operation_info = tk.Label(frame_operation_info, text="Operation Info", anchor=tk.W)  # a title
        title_operation_info.grid(row=0, column=0, sticky=tk.N+tk.W+tk.E)

        info_box_operation = InfoBox(frame_operation_info, text=self.operation_info_box_text, width=250, height=100)
        info_box_operation.grid(row=1, column=0, sticky=tk.N+tk.S+tk.W+tk.E)  # place the frame in the right sidebar
        frame_right_sidebar.rowconfigure(6, weight=1)

    def _init_statusbar(self):
        statusbar = tk.Label(self, textvariable=self.statusbar_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        statusbar.grid(row=1, column=0, columnspan=3, sticky=tk.W+tk.E)

    def on_key_press(self, event):
        if event.keysym == "Return" and self.curr_tool == TOOL_DRAW and self.curr_shape_type != POINT:
            self.end_drawing(event)
        if event.keysym == "Escape":
            self.reset_curr_shape()
        if event.keysym == "BackSpace":
            self.remove_last_vertex()

    def on_left_btn_press(self, event):
        if self.curr_tool == TOOL_DRAW:
            self.add_vertex(event)
        elif self.curr_tool in (TOOL_ERASE, TOOL_INFO, TOOL_OPERATION):
            self.selection_box = MyRectangle(MyPoint(event.x, event.y, name=""))

    def on_left_btn_move(self, event):
        if self.curr_tool == TOOL_DRAW:
            self.move_vertex(event)
        elif self.curr_tool in (TOOL_ERASE, TOOL_INFO, TOOL_OPERATION):
            self._stretch_selection_box(event)

    def on_left_btn_release(self, event):
        if self.curr_tool == TOOL_DRAW:
            self.confirm_vertex(event)
        elif self.curr_tool in (TOOL_ERASE, TOOL_INFO, TOOL_OPERATION):
            self.select_shapes(event)

    def _stretch_selection_box(self, event):
        self.selection_box.v1 = MyPoint(event.x, event.y, name="")  # alter the second vertex of the box
        self.selection_box.id = self._redraw_selection_box()

    def _redraw_selection_box(self):
        if self.selection_box is not None:
            self._erase_selection_box()
            return self._draw_selection_box()

    def _draw_selection_box(self):
        if self.selection_box is not None:
            return self.canvas.create_rectangle(self.selection_box.get_coords())

    def _erase_selection_box(self):
        if self.selection_box is not None:
            self.canvas.delete(self.selection_box.id)

    def erase_shapes(self, canv_ids):
        for canv_id in canv_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                self.canvas.delete(canv_id)

                if shape_id in self.shape_id_to_canvas_text_id:
                    canv_text_id = self.shape_id_to_canvas_text_id[shape_id]
                    self.canvas.delete(canv_text_id)
                    del self.shape_id_to_canvas_text_id[shape_id]

                del self.canvas_id_to_shape_id[canv_id]
                del self.shape_id_to_canvas_id[shape_id]

                if shape_id in self.points:
                    del self.points[shape_id]
                elif shape_id in self.lines:
                    del self.lines[shape_id]
                elif shape_id in self.polygons:
                    del self.polygons[shape_id]
                elif shape_id in self.segments:
                    del self.segments[shape_id]

    def info_shapes(self, canv_ids):
        self.shape_info_box_text.set("")
        for canv_id in canv_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]

                if shape_id in self.points:
                    self.shape_info_box_text.set(self.shape_info_box_text.get() + self.points[shape_id].get_info())
                elif shape_id in self.lines:
                    self.shape_info_box_text.set(self.shape_info_box_text.get() + self.lines[shape_id].get_info())
                elif shape_id in self.polygons:
                    self.shape_info_box_text.set(self.shape_info_box_text.get() + self.polygons[shape_id].get_info())
                elif shape_id in self.segments:
                    self.shape_info_box_text.set(self.shape_info_box_text.get() + self.segments[shape_id].get_info())
                elif shape_id in self.triangles:
                    self.shape_info_box_text.set(self.shape_info_box_text.get() + self.triangles[shape_id].get_info())

                self.shape_info_box_text.set( self.shape_info_box_text.get() + "\n\n")

    def select_shapes(self, event):
        if self.curr_tool in (TOOL_ERASE, TOOL_INFO, TOOL_OPERATION) and isinstance(self.selection_box, MyRectangle):
            sel_box = self.selection_box
            self._erase_selection_box()
            canv_ids = []
            if sel_box.v0 == sel_box.v1:
                canv_ids.extend(event.widget.find_overlapping(event.x, event.y, event.x + 4, event.y + 4))
            else:
                canv_ids.extend(event.widget.find_overlapping(sel_box.v0.x, sel_box.v0.y, sel_box.v1.x, sel_box.v1.y))

            if self.curr_tool == TOOL_ERASE:
                self.erase_shapes(canv_ids)
            elif self.curr_tool in (TOOL_INFO, TOOL_OPERATION):
                self.info_shapes(canv_ids)
                self.selected_canvas_shape_ids = canv_ids

    def add_vertex(self, event):
        if self.curr_tool == TOOL_DRAW and self.curr_shape_type != POINT and len(self.curr_shape) > 0:
            v = MyPoint(event.x, event.y, name="")  # create an anonymous point (i.e., a vertex)
            if self.is_new_vertex(v):  # add it to the shape only if it is different from last added vertex
                self.curr_shape.add_vertex(v)
            self._redraw_curr_shape()

    def move_vertex(self, event):
        if self.curr_tool == TOOL_DRAW and self.curr_shape_type is not None \
                and self.curr_shape_type != POINT and len(self.curr_shape) > 1:
            last_vertex = self.curr_shape.pop_vertex()  # remove the last vertex
            self._erase_vertex(last_vertex)  # and delete it from canvas
            self.add_vertex(event)  # add a new vertex

    def confirm_vertex(self, event):
        x, y = event.x, event.y

        if self.curr_tool == TOOL_DRAW:
            if self.curr_shape_type == POINT:
                self.curr_shape.x, self.curr_shape.y = x, y
                self.end_drawing(None)
            elif (self.curr_shape_type == SEGMENT and len(self.curr_shape) == 2) \
                    or (self.curr_shape_type == TRIANGLE and len(self.curr_shape) == 3):
                self.end_drawing(None)
            else:
                v = MyPoint(x, y, name="")  # create an anonymous point (i.e., a vertex)
                if self.is_new_vertex(v):
                    self.curr_shape.add_vertex(v)

                self._redraw_curr_shape()

    def is_new_vertex(self, v):  # check if the given vertex is "new", i.e., different from the last added
        ret = True
        if len(self.curr_shape) > 0:
            last_vertex = self.curr_shape.vertices[-1]
            if v.x == last_vertex.x and v.y == last_vertex.y:
                ret = False

        return ret

    def end_drawing(self, event):

        if self.curr_shape_type == POINT:
            point = MyPoint(self.curr_shape.x, self.curr_shape.y)
            self._draw_point(point)
            self.points[point.id] = point
        elif self.curr_shape_type == LINE and len(self.curr_shape) >= 2:
            line = MyLine(vertices=self.curr_shape.get_coords(), fill_color=self.curr_shape.fill_color)
            self._draw_line(line, True)
            self.lines[line.id] = line
        elif self.curr_shape_type == POLYGON and len(self.curr_shape) >= 3:
            polygon = MyPolygon(vertices=self.curr_shape.get_coords(), fill_color=self.curr_shape.fill_color)
            self._draw_polygon(polygon, True)
            self.polygons[polygon.id] = polygon
        elif self.curr_shape_type == SEGMENT and len(self.curr_shape) >= 2:
            segment = MySegment(vertices=self.curr_shape.get_coords(), fill_color=self.curr_shape.fill_color)
            self._draw_line(segment, True)
            self.segments[segment.id] = segment
        elif self.curr_shape_type == TRIANGLE and len(self.curr_shape) >= 3:
            triangle = MyTriangle(vertices=self.curr_shape.get_coords(), fill_color=self.curr_shape.fill_color)
            self._draw_polygon(triangle, True)
            self.triangles[triangle.id] = triangle

        self.reset_curr_shape()

    def _draw_point(self, point):
        canv_id = self.canvas.create_oval(point.x-POINT_RADIUS, point.y-POINT_RADIUS,
                                          point.x+POINT_RADIUS, point.y+POINT_RADIUS, fill=point.fill_color.hex_str())
        canv_text_id = self.canvas.create_text(point.x, point.y, text=point.name, anchor=tk.NW)

        self.shape_id_to_canvas_id[point.id] = canv_id
        self.canvas_id_to_shape_id[canv_id] = point.id
        self.shape_id_to_canvas_text_id[point.id] = canv_text_id

    def _draw_line(self, line, draw_text=False):
        if len(line) > 1:
            canv_id = self.canvas.create_line(line.get_coords(), fill=line.fill_color.hex_str())
            self.shape_id_to_canvas_id[line.id] = canv_id
            self.canvas_id_to_shape_id[canv_id] = line.id

            if draw_text:
                central_vertex = line.central_vertex()

                canv_text_id = self.canvas.create_text(central_vertex.x, central_vertex.y, text=line.name, anchor=tk.NW)
                self.shape_id_to_canvas_text_id[line.id] = canv_text_id

    def _draw_polygon(self, polygon, draw_text=False):
        if len(polygon) > 2:
            canv_id = self.canvas.create_polygon(polygon.get_coords(), fill=polygon.fill_color.hex_str())
            self.shape_id_to_canvas_id[polygon.id] = canv_id
            self.canvas_id_to_shape_id[canv_id] = polygon.id

            if draw_text:
                centroid = polygon.centroid()

                canv_text_id = self.canvas.create_text(int(centroid.x), int(centroid.y), text=polygon.name)
                self.shape_id_to_canvas_text_id[polygon.id] = canv_text_id

    def _redraw_curr_shape(self):
        self._erase_curr_shape()
        self._draw_curr_shape()

    def _draw_curr_shape(self):
        if len(self.curr_shape) > 0:
            for v in self.curr_shape.vertices:
                self._draw_vertex(v)

            if self.curr_shape_type == LINE or self.curr_shape_type == SEGMENT \
                    or ((self.curr_shape_type == POLYGON or self.curr_shape_type == TRIANGLE) and len(self.curr_shape) < 3):
                self._draw_line(self.curr_shape)
            elif self.curr_shape_type == POLYGON or self.curr_shape_type == TRIANGLE:
                self._draw_polygon(self.curr_shape)

    def _erase_curr_shape(self):
        if self.curr_shape is not None:
            shape_id = self.curr_shape.id
            if shape_id in self.shape_id_to_canvas_id:
                self.erase_shapes([self.shape_id_to_canvas_id[shape_id]])

            if hasattr(self.curr_shape, 'vertices'):
                for v in self.curr_shape.vertices:
                    self._erase_vertex(v)

    def _draw_vertex(self, v):
        canv_id1 = self.canvas.create_line(v.x-VERTEX_RADIUS, v.y+VERTEX_RADIUS,
                                           v.x+VERTEX_RADIUS, v.y-VERTEX_RADIUS, fill="black")
        v_id1 = str(v.id) + "_1"
        self.canvas_id_to_shape_id[canv_id1] = v_id1
        self.shape_id_to_canvas_id[v_id1] = canv_id1

        canv_id2 = self.canvas.create_line(v.x-VERTEX_RADIUS, v.y-VERTEX_RADIUS,
                                           v.x+VERTEX_RADIUS, v.y+VERTEX_RADIUS, fill="black")
        v_id2 = str(v.id) + "_2"
        self.canvas_id_to_shape_id[canv_id2] = v_id2
        self.shape_id_to_canvas_id[v_id2] = canv_id2

    def _erase_vertex(self, v):
        v_id1 = str(v.id)+"_1"
        v_id2 = str(v.id)+"_2"
        if v_id1 in self.shape_id_to_canvas_id:
            canv_id1 = self.shape_id_to_canvas_id[v_id1]
            canv_id2 = self.shape_id_to_canvas_id[v_id2]

            self.canvas.delete(canv_id1)
            del self.shape_id_to_canvas_id[v_id1]
            del self.canvas_id_to_shape_id[canv_id1]
            self.canvas.delete(canv_id2)
            del self.shape_id_to_canvas_id[v_id2]
            del self.canvas_id_to_shape_id[canv_id2]

    def change_tool(self, new_tool, new_shape=None):
        old_tool = self.curr_tool
        old_shape = self.curr_shape_type

        if new_tool != old_tool or new_shape != old_shape:
            self.curr_tool = new_tool
            self.curr_shape_type = new_shape
            self.reset_curr_shape()
            self.set_statusbar()
            self.set_info_box()

    def reset_curr_shape(self):
        self._erase_curr_shape()

        if self.curr_shape_type == POINT:
            self.curr_shape = MyPoint(name="")
        elif self.curr_shape_type == LINE:
            self.curr_shape = MyLine(name="")
        elif self.curr_shape_type == POLYGON:
            self.curr_shape = MyPolygon(name="")
        elif self.curr_shape_type == SEGMENT:
            self.curr_shape = MySegment(name="")
        elif self.curr_shape_type == TRIANGLE:
            self.curr_shape = MyTriangle(name="")

    def set_info_box(self):
        if self.curr_tool == TOOL_DRAW and self.curr_shape_type is not None:
            self.info_box_text.set(INFO[self.curr_tool][self.curr_shape_type])
        elif self.curr_tool is not None:
            self.info_box_text.set(INFO[self.curr_tool])

    def set_statusbar(self):
        if self.curr_tool == TOOL_DRAW and self.curr_shape_type is not None:
            self.statusbar_text.set(STATUS[self.curr_tool][self.curr_shape_type])
        elif self.curr_tool is not None:
            self.statusbar_text.set(STATUS[self.curr_tool])

    def remove_last_vertex(self):
        if self.curr_shape is not None and self.curr_shape_type != POINT and len(self.curr_shape) > 0:
            last_vertex = self.curr_shape.pop_vertex()
            self._erase_vertex(last_vertex)
            self._redraw_curr_shape()

    def perform_operation(self):
        if self.curr_tool == TOOL_OPERATION:
            if len(self.selected_canvas_shape_ids) == 0:
                self.operation_info_box_text.set("No shape selected. Please select some shapes.")
            else:
                op = self.operation_var.get()
                if op == OPERATION_POINT_IN_POLY:
                    self.perform_point_in_polygon()
                elif op == OPERATION_SEGMENT_INTERSECT:
                    self.perform_segment_intersects()
                elif op == OPERATION_SEGMENT_INTERSECTION:
                    self.perform_segment_intersection()
                elif op == OPERATION_N_SEGMENT_INTERSECTION:
                    self.perform_n_segment_intersection()
                elif op == OPERATION_CONVEX_HULL_GRAHAM_PLAIN:
                    self.perform_graham_plain()
                elif op == OPERATION_CONVEX_HULL_GRAHAM_PRECISE:
                    self.perform_graham_precise()
                elif op == OPERATION_SPIRAL:
                    self.perform_spiral()
                elif op == OPERATION_SPIRAL_PRECISE:
                    self.perform_spiral_precise()

    def perform_graham_precise(self):
        selected_points = []

        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.points:
                    selected_points.append(self.points[shape_id])

        if len(selected_points) < 4:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least four points to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            CH = convex_hull_graham_precise(selected_points)
            if len(CH) > 0:
                output_text = "CH=["
                for p in CH.vertices:
                    output_text += p.get_name() + ", "
                output_text += "]"
                self.operation_info_box_text.set(str(output_text))

                self._draw_line(CH)  # draw the CH on canvas (it is a MyLine)
                self.lines[CH.id] = CH  # add the CH to the line list



    def perform_graham_plain(self):
        selected_points = []

        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.points:
                    selected_points.append(self.points[shape_id])

        if len(selected_points) < 4:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least four points to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            CH = convex_hull_graham_plain(selected_points)
            if len(CH) > 0:
                output_text = "CH=["
                for p in CH.vertices:
                    output_text += p.get_name() + ", "
                output_text += "]"
                self.operation_info_box_text.set(str(output_text))

                self._draw_line(CH)  # draw the CH on canvas (it is a MyLine)
                self.lines[CH.id] = CH  # add the CH to the line list



    def perform_spiral(self):

        selected_points = []

        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.points:
                    selected_points.append(self.points[shape_id])

        if len(selected_points) < 4:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least four points to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            spiral = make_spiral(selected_points)
            if len(spiral) > 0:
                output_text = "SP=["
                for p in spiral.vertices:
                    output_text += p.get_name() + ", "
                output_text += "]"
                self.operation_info_box_text.set(str(output_text))

                self._draw_line(spiral)  # draw the CH on canvas (it is a MyLine)
                self.lines[spiral.id] = spiral  # add the CH to the line list


    def perform_spiral_precise(self):

        selected_points = []

        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.points:
                    selected_points.append(self.points[shape_id])

        if len(selected_points) < 4:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least four points to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            spiral = make_spiral_precise(selected_points)
            if len(spiral) > 0:
                output_text = "SP=["
                for p in spiral.vertices:
                    output_text += p.get_name() + ", "
                output_text += "]"
                self.operation_info_box_text.set(str(output_text))

                self._draw_line(spiral)  # draw the CH on canvas (it is a MyLine)
                self.lines[spiral.id] = spiral  # add the CH to the line list


    def perform_n_segment_intersection(self):
        segments = []

        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.segments:
                    segments.append(self.segments[shape_id])

        if len(segments) < 2:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least two segments to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            intersection_points = n_line_intersection(segments)
            self.operation_info_box_text.set(
                                str(intersection_points)
            )
            for inter_p in intersection_points:
                self._draw_point(inter_p)  # draw the point on canvas
                self.points[inter_p.id] = inter_p  # add the point to the point list


    def perform_point_in_polygon(self):
        polys = []
        points = []
        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.points:
                    points.append(self.points[shape_id])
                elif shape_id in self.polygons:
                    polys.append(self.polygons[shape_id])
                elif shape_id in self.triangles:
                    polys.append(self.triangles[shape_id])

        if len(polys) == 0 or len(points) == 0:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least a point and a polygon to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            for poly in polys:
                for p in points:
                    self.operation_info_box_text.set(self.operation_info_box_text.get() +
                                                     poly.name + "-" + p.name + ":" +
                                                     str(poly.is_point_in(p)))
                    self.operation_info_box_text.set( self.operation_info_box_text.get() + "\n\n")

    def perform_segment_intersects(self):
        segments = []
        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.segments:
                    segments.append(self.segments[shape_id])

        if len(segments) == 0:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least two segments to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            for i in range(len(segments)):
                for j in range(i+1, len(segments)):
                    self.operation_info_box_text.set(self.operation_info_box_text.get() +
                                                     segments[i].name + "-" + segments[j].name + ":" +
                                                     str(segments[i].intersects(segments[j])))
                    self.operation_info_box_text.set( self.operation_info_box_text.get() + "\n\n")

    def perform_segment_intersection(self):
        segments = []
        for canv_id in self.selected_canvas_shape_ids:
            if canv_id in self.canvas_id_to_shape_id:
                shape_id = self.canvas_id_to_shape_id[canv_id]
                if shape_id in self.segments:
                    segments.append(self.segments[shape_id])

        if len(segments) == 0:
            self.operation_info_box_text.set("The selected geometries are inappropriate for this operation."
                                             "This operation requires at least two segments to "
                                             "be selected.")
        else:
            self.operation_info_box_text.set("")
            for i in range(len(segments)):
                for j in range(i+1, len(segments)):
                    self.operation_info_box_text.set(self.operation_info_box_text.get() +
                                                     segments[i].name + "-" + segments[j].name + ":" +
                                                     str(segments[i].segment_intersection(segments[j])))
                    self.operation_info_box_text.set( self.operation_info_box_text.get() + "\n\n")

if __name__ == "__main__":
    app = MyDrawingApp()
    app.title("Simple Geometry Input App (" + str(VERSION) + ")")
    app.mainloop()