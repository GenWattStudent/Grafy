from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.ui.GraphCanvas import GraphCanvas
from src.utils.Vector import Vector
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.elements.Intersection import Intersection

class CanvasHelper:
    def __init__(self, canvas: GraphModelCanvas):
        self.canvas = canvas

    def canvas_to_graph_coords(self, canvas_x, canvas_y):
        screen_x = self.canvas.canvasx(0)
        screen_y = self.canvas.canvasy(0)
        return canvas_x + screen_x, canvas_y + screen_y

    def graph_to_canvas_coords(self, graph_x, graph_y):
        screen_x = self.canvas.canvasx(0)
        screen_y = self.canvas.canvasy(0)
        return graph_x - screen_x, graph_y - screen_y
    
    def find_elemment_under_cursor(self, event, elements: list[Intersection | Node | Edge]) -> Intersection | Node | Edge | None:
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for element in elements:
            if element.is_under_cursor(Vector(x, y)):
                return element
        return None
