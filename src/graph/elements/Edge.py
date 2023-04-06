from src.graph.elements.Node import Node
import tkinter as tk


class Edge:
    def __init__(self, node1: Node, node2: Node, distance: float | None = None, color: str = 'white'):
        self.node1 = node1
        self.node2 = node2
        self.is_dragged: bool = False
        self.is_path: bool = False
        self.distance = distance
        self.color = color
        self.path_color = 'red'
        self.canvas_id: tk._CanvasItemId | None = None

    def get_color(self) -> str:
        if self.is_path:
            return self.path_color
        else:
            return self.color

    def draw(self, canvas: tk.Canvas):
        color = self.get_color()

        self.canvas_id = canvas.create_line(
            self.node1.position.x, self.node1.position.y, self.node2.position.x, self.node2.position.y, fill=color,
            width=2, tags="edge")
