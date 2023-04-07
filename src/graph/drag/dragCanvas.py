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
from src.ui.Toolbar import Tools


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

        self.node_1 = None
        self.node_2 = None

        self.canvas.bind("<Motion>", self.motion)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-1>", self.click)

    def motion(self, event):
        self.canvas.change_cursor(event)
        if self.graph.is_toolbar() and self.graph.toolbar.get_selected_tool() == Tools.ADD_NODE:
            self.show_node_preview(event)
        elif self.graph.is_toolbar() and self.graph.toolbar.get_prev_tool() == Tools.ADD_EDGE:
            if self.node_preview:
                self.node_preview.delete(self.canvas)
                self.node_preview = None

    def show_node_preview(self, event):
        if self.node_preview:
            self.node_preview.delete(self.canvas)
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        self.node_preview = Node(Vector(x, y), len(self.graph.nodes),  self.draw_config.node_radius)
        self.node_preview.draw(self.canvas)

    def add_node(self, node: Node | None):
        if node:
            node.delete(self.canvas)
            self.graph.add_node(node)
            self.node_preview = None
            self.canvas.draw_nodes(self.graph.nodes)

    def add_edge(self, event):
        if self.graph.is_toolbar() and self.graph.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            for node in self.graph.nodes:
                if node.is_under_cursor(Vector(event.x, event.y)):
                    if not self.node_1:
                        self.node_1 = node
                        self.graph.generator.select_nodes(self.node_1)
                    else:
                        self.graph.add_edge(Edge(self.node_1, node))
                        self.canvas.draw_nodes_and_edges()
                        self.node_1 = None
                        self.node_2 = None
                        self.graph.generator.unselect_nodes()
                        break
        elif self.graph.is_toolbar() and self.graph.toolbar.is_cleaned and self.graph.toolbar.get_prev_tool() == Tools.ADD_EDGE:
            self.graph.generator.unselect_nodes()
            self.node_1 = None
            self.node_2 = None
            self.graph.toolbar.is_cleaned = True

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

    def select(self, node: Node):
        if self.graph.is_toolbar() and self.graph.toolbar.get_selected_tool() == Tools.SELECT:
            self.graph.generator.select_nodes(node)
            self.canvas.draw_nodes(self.graph.nodes)
        elif self.graph.is_toolbar() and self.graph.toolbar.get_prev_tool() == Tools.SELECT:
            self.graph.generator.unselect_nodes()
            self.canvas.draw_nodes(self.graph.nodes)

    def drag_node(self, event):
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for node in self.graph.nodes:
            if node.is_under_cursor(Vector(x, y)):
                self.select(node)
                self.draging_node = node
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.graph.generator.set_dragged_edges(self.graph.edges, node)

    def drag_canvas(self, event):
        if not self.draging_node:
            self.canvas.scan_mark(event.x, event.y)

    def click(self, event):
        self.canvas.focus_set()
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
