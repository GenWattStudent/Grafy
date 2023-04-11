from src.graph.elements.Node import Node
import tkinter as tk
from src.Theme import Theme
from src.utils.Vector import Vector
from src.graph.elements.CanvasElement import CanvasElement


class Edge(CanvasElement):
    def __init__(self, node1: Node, node2: Node, distance: float | None = None, color: str = 'white'):
        super().__init__(color)
        self.node1 = node1
        self.node2 = node2
        self.is_path: bool = False
        self.distance = distance
        self.path_color = Theme.get("edge_path_color")
        self.dragged_color = Theme.get("edge_dragged_color")
        self.selected_color = Theme.get("edge_selected_color")
        self.id = f"{node1.id}-{node2.id}"

    def is_under_cursor(self, cursor_position: Vector, threshold: float = 5) -> bool:
        x1, y1 = self.node1.position.x, self.node1.position.y
        x2, y2 = self.node2.position.x, self.node2.position.y
        cursor_x, cursor_y = cursor_position.x, cursor_position.y

        distance = abs((y2 - y1) * cursor_x - (x2 - x1) * cursor_y + x2 * y1 - y2 * x1) / ((y2 - y1)
                                                                                           ** 2 + (x2 - x1) ** 2) ** 0.5 + 0.001
        return distance <= threshold

    def get_color(self) -> str:
        if self.is_path:
            return self.path_color
        elif self.is_dragged:
            return self.dragged_color
        elif self.is_selected:
            return self.selected_color
        else:
            return self.color

    def draw(self, canvas: tk.Canvas):
        color = self.get_color()

        self.canvas_id = canvas.create_line(
            self.node1.position.x, self.node1.position.y, self.node2.position.x, self.node2.position.y, fill=color,
            width=2, tags="edge")

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Edge):
            return self.id == __value.id
        return False
