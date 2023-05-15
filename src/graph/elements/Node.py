from src.utils.Vector import Vector
import tkinter as tk
from tkinter.font import Font
import ttkbootstrap as ttk
from src.Theme import theme
from src.graph.elements.CanvasElement import CanvasElement 

class Node(CanvasElement):
    def __init__(self, position: Vector, index: int, width: int = 200, height: int = 100):
        super().__init__(theme.get("primary"))
        self.index: int = index
        self.value: str = str(index)
        self.position: Vector = position
        self.width: int = width
        self.min_width: int = 120
        self.height: int = height
        self.selected_color: str = theme.get("secondary")
        self.border_color: str = theme.get("border")
        self.dragged_color: str = theme.get("success")
        self.text: tk._CanvasItemId | None = None
        self.font = Font(family="Arial", size=20)

    def delete(self, canvas: ttk.Canvas):
        self.is_dragged = False
        self.is_selected = False
        if self.canvas_id and self.text:
            canvas.delete(self.canvas_id)
            canvas.delete(self.text)

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        x1 = self.position.x
        y1 = self.position.y
        x2 = x1 + self.width
        y2 = y1 + self.height
        if cursor_position.x >= x1 and cursor_position.x <= x2 and cursor_position.y >= y1 and cursor_position.y <= y2:
            return True
        return False

    def get_color(self) -> str:
        if self.is_selected:
            return self.selected_color
        elif self.is_dragged:
            return self.dragged_color
        else:
            return self.color
        
    def update_width_depends_on_value(self):
        new_width = self.font.measure(self.value) + 20
        if new_width > self.min_width:
            self.width = new_width
        else:
            self.width = self.min_width

    def draw(self, canvas: ttk.Canvas):
        color = self.get_color()
        x1 = self.position.x
        y1 = self.position.y

        self.update_width_depends_on_value()

        self.canvas_id = canvas.create_rectangle(x1, y1, x1 + self.width, y1 + self.height, fill=color, outline=self.border_color, width=2)
        self.text = canvas.create_text(x1 + self.width / 2, y1 + self.height / 2, text=self.value, fill=theme.get('fg'), font=self.font)

    def get_index(self) -> int:
        return self.index - 1

    def __hash__(self):
        return hash((self.position, self.index))

    def __str__(self):
        return f"Node({self.index}, {self.position})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: "Node") -> bool:
        return self.id == other.id

    def distance(self, other: "Node"):
        return (self.position - other.position).length()
