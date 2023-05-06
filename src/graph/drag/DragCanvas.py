from __future__ import annotations
from abc import ABC, abstractmethod
from src.graph.GraphModel import GraphModel
from src.graph.DrawGraphConfig import DrawGraphConfig
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ui.GraphCanvas import GraphCanvas
from src.utils.Vector import Vector
from src.graph.helpers.CanvasHelper import CanvasHelper
from src.utils.Event import Event
from copy import copy

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
    def __init__(self, canvas: GraphCanvas, draw_config: DrawGraphConfig, graph: GraphModel):
        self.draging_node = None
        self.x = 0
        self.y = 0
        self.node_old_position: Vector | None = None
        self.canvas = canvas
        self.draw_config = draw_config
        self.graph = graph
        self.is_drag_node = True
        self.canvas_helper =  CanvasHelper(self.canvas)
        self.on_element_move_end_event = Event()
        self.on_element_move_start_event = Event()

    def on_element_move(self, callback):
        self.on_element_move_end_event += callback
    
    def off_element_move(self, callback):
        self.on_element_move_end_event -= callback

    def on_element_move_start(self, callback):
        self.on_element_move_start_event += callback
    
    def off_element_move_start(self, callback):
        self.on_element_move_start_event -= callback

    def motion(self, event):
        self.canvas.change_cursor(event)

    def drag(self, event):
        print(self.draging_node)
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
                self.node_old_position = copy(node.position)
                self.on_element_move_start_event(self.draging_node, Vector(x, y))
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.graph.generator.set_dragged_edges(self.graph.edges, node)

    def drag_canvas(self, event):
        if not self.draging_node:
            self.canvas.scan_mark(event.x, event.y)

    def click(self, event):
        if self.is_drag_node:
            self.drag_node(event)
        if not self.draging_node:
            self.drag_canvas(event)

    def end_drag(self, event):
        if self.draging_node:
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            self.draging_node.is_dragged = False
            self.draging_node.radius = self.draw_config.node_radius
            self.graph.generator.set_dragged_edges(self.graph.edges, self.draging_node, False)
            self.on_element_move_end_event(self.draging_node, Vector(x, y), self.node_old_position)
            self.draging_node = None
            return

        self.canvas.scan_dragto(event.x, event.y, gain=1)

