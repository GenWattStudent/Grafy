from __future__ import annotations
from abc import ABC, abstractmethod
from src.graph.Graph import Graph
from src.graph.DrawGraphConfig import DrawGraphConfig
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ui.GraphCanvas import GraphCanvas
from src.utils.Vector import Vector
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.elements.Intersection import Intersection
from src.ui.Toolbar import Tools
from src.Theme import Theme
from src.state.GraphState import graph_state


class Draggable(ABC):
    @abstractmethod
    def drag(self, event):
        pass

    @abstractmethod
    def click(self, event):
        pass

    @abstractmethod
    def end_drag(self, event):
        pass


class DragCanvas(Draggable):
    def __init__(self, canvas: "GraphCanvas", draw_config: DrawGraphConfig, graph: Graph):
        self.draging_node = None
        self.node_preview = None
        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.draw_config = draw_config
        self.graph = graph

        # self.canvas.bind("<Motion>", self.motion)
        # self.canvas.bind("<B1-Motion>", self.drag)
        # self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        # self.canvas.bind("<Button-1>", self.click)

        if self.graph.toolbar:
            self.graph.toolbar.selected_tool.subscribe(self.on_tool_change)

    def on_tool_change(self, tool: Tools):
        if self.graph.toolbar.get_prev_tool() == Tools.SELECT:
            self.graph.deselect()
            self.canvas.draw_nodes_and_edges()
        elif self.graph.toolbar.get_prev_tool() == Tools.ADD_EDGE:
            self.graph.toolbar.deselect_all_tool()
            self.canvas.draw_nodes(self.graph.nodes)
        elif self.graph.toolbar.get_prev_tool() == Tools.ADD_NODE and self.node_preview:
            self.node_preview.delete(self.canvas)
            self.node_preview = None
        if self.graph.toolbar.get_selected_tool() == Tools.DELETE:
            self.canvas.draw_graph()

    def motion(self, event):
        self.canvas.change_cursor(event)
        if self.graph.is_toolbar() and self.graph.toolbar.get_selected_tool() == Tools.ADD_NODE:
            self.show_node_preview(event)

    def show_node_preview(self, event):
        if self.node_preview:
            self.node_preview.delete(self.canvas)
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        pos = Vector(x, y)
        index = 1
        if len(self.graph.nodes) > 0:
            index = len(self.graph.nodes) + 1
        self.node_preview = Node(pos, index, self.draw_config.node_radius,
                                 Theme.get("node_color"), Theme.get("node_selected_color"))
        self.node_preview.draw(self.canvas)

    def add_node(self, node: Node | None):
        if node:
            node.delete(self.canvas)
            self.graph.add_node(node)
            self.node_preview = None
            self.canvas.draw_nodes(self.graph.nodes)

    def add_edge(self, event):
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        if self.graph.is_toolbar() and self.graph.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            for node in self.graph.nodes:
                if node.is_under_cursor(Vector(x, y)):
                    if len(self.graph.toolbar.selected_elements) == 0:
                        self.graph.toolbar.select_tool(node)
                    else:
                        self.graph.add_edge(Edge(self.graph.toolbar.selected_elements[0], node))
                        self.graph.toolbar.deselect_all_tool()
                        self.canvas.draw_nodes_and_edges()
                        break

    def drag(self, event):
        if self.draging_node:
            x, y = self.canvas_to_graph_coords(event.x, event.y)
            self.draging_node.position.x = x
            self.draging_node.position.y = y
            self.draging_node.is_dragged = True
            self.canvas.delete("all")
            self.canvas.draw_edges(self.graph.edges)
            self.canvas.draw_nodes(self.graph.nodes)
            return

        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def select(self, event):
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        if self.graph.toolbar and self.graph.toolbar.get_selected_tool() == Tools.SELECT:
            for element in self.graph.get_graph_elements():
                if element.is_under_cursor(Vector(x, y)):
                    self.graph.toolbar.select_tool(element)
                    self.canvas.draw_nodes_and_edges()
                    break

    def find_elemment_under_cursor(self, event) -> Intersection | Node | Edge | None:
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for element in self.graph.get_graph_elements():
            if element.is_under_cursor(Vector(x, y)):
                return element
        return None

    def drag_node(self, event):
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for node in self.graph.nodes:
            if node.is_under_cursor(Vector(x, y)):
                self.draging_node = node
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.graph.generator.set_dragged_edges(self.graph.edges, node)

    def drag_canvas(self, event):
        if not self.draging_node:
            self.canvas.scan_mark(event.x, event.y)

    def click(self, event):
        self.canvas.focus_set()
        self.select(event)
        self.add_node(self.node_preview)
        self.drag_node(event)
        self.drag_canvas(event)
        self.add_edge(event)

    def end_drag(self, event):
        if self.draging_node:
            self.draging_node.is_dragged = False
            self.draging_node.radius = self.draw_config.node_radius

            self.graph.generator.set_dragged_edges(self.graph.edges, self.draging_node, False)
            self.draging_node = None
            self.canvas.draw_graph()
            graph_state.set(self.graph)
            return

        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def canvas_to_graph_coords(self, canvas_x, canvas_y):
        screen_x = self.canvas.canvasx(0)
        screen_y = self.canvas.canvasy(0)
        return canvas_x + screen_x, canvas_y + screen_y

    def graph_to_canvas_coords(self, graph_x, graph_y):
        screen_x = self.canvas.canvasx(0)
        screen_y = self.canvas.canvasy(0)
        return graph_x - screen_x, graph_y - screen_y
