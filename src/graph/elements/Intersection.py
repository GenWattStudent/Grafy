from src.utils.Vector import Vector
import tkinter as tk
import uuid


class Intersection:
    def __init__(self, position: Vector, color: str = 'yellow', radius: int = 4):
        self.position = position
        self.color = color
        self.canvas_id: tk._CanvasItemId | None = None
        self.radius = radius
        self.id = uuid.uuid4()
        self.is_selected = False

    def delete(self, canvas: tk.Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)

    def draw(self, canvas: tk.Canvas):
        if self.canvas_id:
            canvas.delete(self.canvas_id)

        self.canvas_id = canvas.create_oval(self.position.x - self.radius, self.position.y - self.radius,
                                            self.position.x + self.radius, self.position.y + self.radius,
                                            fill=self.color, tags="intersection")

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        return (self.position - cursor_position).length() <= self.radius
