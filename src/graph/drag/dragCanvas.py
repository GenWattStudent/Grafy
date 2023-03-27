from __future__ import annotations
from abc import ABC, abstractmethod
from src.graph.Graph import Graph
from src.graph.DrawGraphConfig import DrawGraphConfig
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ui.GraphCanvas import GraphCanvas
from src.utils.Vector import Vector


class Draggable(ABC):
    @abstractmethod
    def drag(self, event):
        pass

    @abstractmethod
    def start_drag(self, event):
        pass

    @abstractmethod
    def end_drag(self, event):
        pass


class DragCanvas(Draggable):
    def __init__(self, canvas: "GraphCanvas", draw_config: DrawGraphConfig, graph: Graph):
        self.draging_node = None
        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.draw_config = draw_config
        self.graph = graph

        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)
        self.canvas.bind("<Button-1>", self.start_drag)

    def drag(self, event):
        if self.draging_node:
            x, y = self.canvas_to_graph_coords(event.x, event.y)
            self.draging_node.position.x = x
            self.draging_node.position.y = y
            self.canvas.delete("all")
            self.canvas.draw_edges(self.graph.edges)
            self.canvas.draw_nodes(self.graph.nodes)
            return
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def start_drag(self, event):
        self.canvas.focus_set()

        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for node in self.graph.nodes:
            if node.is_under_cursor(Vector(x, y)):
                node.is_selected = True
                self.graph.generator.select_nodes(node)
                self.draging_node = node
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.graph.generator.set_dragged_edges(self.graph.edges, node)
        if not self.draging_node:
            self.canvas.scan_mark(event.x, event.y)

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
