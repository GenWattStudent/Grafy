from src.utils.Vector import Vector
from abc import abstractmethod, ABC
import tkinter as tk
import uuid

class CanvasElement(ABC):
    def __init__(self, color: str):
        self.position: Vector = Vector(0, 0)
        self.color = color
        self.canvas_id: tk._CanvasItemId | None = None
        self.id = uuid.uuid4()  
        self.is_selected = False
        self.is_dragged = False

    def delete(self, canvas: tk.Canvas):
        self.is_dragged = False
        self.is_selected = False
        if self.canvas_id:
            canvas.delete(self.canvas_id)

    @abstractmethod
    def draw(self, canvas: tk.Canvas):
        pass 

    @abstractmethod
    def is_under_cursor(self, cursor_position: Vector) -> bool:
        pass
    