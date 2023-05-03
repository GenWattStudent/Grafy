from src.utils.Vector import Vector
import tkinter as tk
from src.Theme import theme
from src.graph.elements.CanvasElement import CanvasElement 


class Node(CanvasElement):
    def __init__(
            self, position: Vector, index: int, radius: int = 15, color: str = 'red', selected_color: str = 'blue',
            border_color: str = 'white'):
        super().__init__(color)
        self.index: int = index
        self.position: Vector = position
        self.radius: int = radius
        self.selected_color: str = selected_color
        self.border_color: str = border_color
        self.dragged_color: str = theme.get("success")
        self.text: tk._CanvasItemId | None = None

    def delete(self, canvas: tk.Canvas):
        self.is_dragged = False
        self.is_selected = False
        if self.canvas_id and self.text:
            canvas.delete(self.canvas_id)
            canvas.delete(self.text)

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        return (self.position - cursor_position).length() <= self.radius

    def get_color(self) -> str:
        if self.is_selected:
            return self.selected_color
        elif self.is_dragged:
            return self.dragged_color
        else:
            return self.color

    def draw(self, canvas: tk.Canvas):
        color = self.get_color()

        self.canvas_id = canvas.create_oval(
            self.position.x - self.radius, self.position.y - self.radius, self.position.x + self.radius, self.position.y +
            self.radius, fill=color, outline=self.border_color, width=2, tags=("node", str(self.index)))
        self.text = canvas.create_text(
            self.position.x, self.position.y, text=str(self.index), fill="white", tags="node")

    def get_index(self) -> int:
        return self.index - 1

    def __hash__(self):
        return hash((self.position, self.index, self.radius))

    def __str__(self):
        return f"Node({self.index}, {self.position}, {self.radius})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Node") -> bool:
        return self.id == other.id

    def distance(self, other: "Node"):
        return (self.position - other.position).length()
