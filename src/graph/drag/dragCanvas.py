from __future__ import annotations
from abc import ABC, abstractmethod
from src.graph.Graph import Graph
from src.graph.DrawGraphConfig import DrawGraphConfig
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ui.GraphCanvas import GraphCanvas
from src.utils.Vector import Vector
from src.graph.helpers.CanvasHelper import CanvasHelper
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
    def __init__(self, canvas: GraphCanvas, draw_config: DrawGraphConfig, graph: Graph):
        self.draging_node = None
        self.x = 0
        self.y = 0
        self.canvas = canvas
        self.draw_config = draw_config
        self.graph = graph
        self.canvas_helper =  CanvasHelper(canvas)

    def motion(self, event):
        self.canvas.change_cursor(event)

    def drag(self, event):
        if self.draging_node:
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            self.draging_node.position.x = x
            self.draging_node.position.y = y
            self.draging_node.is_dragged = True
            self.canvas.delete("all")
            self.canvas.draw_edges(self.graph.edges)
            self.canvas.draw_nodes(self.graph.nodes)
            return

        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def drag_node(self, event):
        x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
        for node in self.graph.nodes:
            if node.is_under_cursor(Vector(x, y)):
                self.draging_node = node
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.graph.generator.set_dragged_edges(self.graph.edges, node)

    def drag_canvas(self, event):
        if not self.draging_node:
            self.canvas.scan_mark(event.x, event.y)

    def click(self, event):
        self.drag_node(event)
        self.drag_canvas(event)

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

