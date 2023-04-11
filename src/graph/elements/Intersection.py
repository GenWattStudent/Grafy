from src.utils.Vector import Vector
from src.graph.elements.CanvasElement import CanvasElement
import tkinter as tk

class Intersection(CanvasElement):
    def __init__(self, position: Vector, color: str = 'yellow', radius: int = 4):
        super().__init__(color)
        self.position = position
        self.radius = radius

    def draw(self, canvas: tk.Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)

        self.canvas_id = canvas.create_oval(self.position.x - self.radius, self.position.y - self.radius,
                                            self.position.x + self.radius, self.position.y + self.radius,
                                            fill=self.color, tags="intersection")

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        return (self.position - cursor_position).length() <= self.radius
