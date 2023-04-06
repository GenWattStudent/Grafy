from src.utils.Vector import Vector
import tkinter as tk


class Node:
    def __init__(
            self, position: Vector, index: int, radius: int = 15, color: str = 'red', selected_color: str = 'blue',
            border_color: str = 'white'):
        self.index: int = index
        self.position: Vector = position
        self.radius: int = radius
        self.is_dragged: bool = False
        self.is_selected: bool = False
        self.color: str = color
        self.selected_color: str = selected_color
        self.border_color: str = border_color
        self.canvas_id: tk._CanvasItemId | None = None

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        return (self.position - cursor_position).length() <= self.radius

    def get_color(self) -> str:
        if self.is_selected:
            return self.selected_color
        else:
            return self.color

    def draw(self, canvas: tk.Canvas):
        color = self.get_color()

        if self.canvas_id:
            canvas.delete(self.canvas_id)

        self.canvas_id = canvas.create_oval(
            self.position.x - self.radius, self.position.y - self.radius, self.position.x + self.radius, self.position.y +
            self.radius, fill=color, outline=self.border_color, width=2, tags=("node", str(self.index)))
        canvas.create_text(self.position.x, self.position.y, text=str(self.index), fill="white", tags="node")

    def get_index(self) -> int:
        return self.index - 1

    def __hash__(self):
        return hash((self.position, self.index, self.radius))

    def __str__(self):
        return f"Node({self.index}, {self.position}, {self.radius})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.index == other.index

    def distance(self, other: "Node"):
        return (self.position - other.position).length()
