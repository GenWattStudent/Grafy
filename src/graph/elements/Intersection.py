from src.utils.Vector import Vector
from src.graph.elements.CanvasElement import CanvasElement
import tkinter as tk
from src.Theme import theme

class Intersection(CanvasElement):
    def __init__(self, position: Vector, color: str = 'yellow', radius: int = 4, group_size: int = 1):
        super().__init__(color)
        self.position = position
        self.radius = radius
        self.group_size = group_size
        self.text_id = None

    def delete(self, canvas: tk.Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)
        if self.text_id:
            canvas.delete(self.text_id)

    def draw(self, canvas: tk.Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)

        self.canvas_id = canvas.create_oval(self.position.x - self.radius, self.position.y - self.radius,
                                            self.position.x + self.radius, self.position.y + self.radius,
                                            fill=self.color, tags="intersection")
        
        self.text_id = canvas.create_text(self.position.x, self.position.y, text=str(self.group_size), fill=theme.get("fg"), font=("Arial", 16))

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        return (self.position - cursor_position).length() <= self.radius
