from src.graph.elements.Node import Node
import tkinter as tk
from src.Theme import theme
from src.utils.Vector import Vector
from src.graph.elements.CanvasElement import CanvasElement

class Edge(CanvasElement):
    def __init__(self, node1: Node, node2: Node, distance: float | None = None, color: str = 'white', to_node1: int = 0, to_node2: int = 0):
        super().__init__(color)
        self.start_point = Vector(0, 0)
        self.end_point = Vector(0, 0)
        self.node1 = node1
        self.node2 = node2
        self.is_path: bool = False
        self.distance = distance
        self.path_color = theme.get("danger")
        self.dragged_color = theme.get("success")
        self.selected_color = theme.get("selectbg")
        self.id = f"{node1.id}-{node2.id}"
        self.to_node1 = to_node1
        self.to_node2 = to_node2

    def delete(self, canvas: tk.Canvas):
        self.is_dragged = False
        self.is_selected = False
        canvas.delete(self.line_id)
        canvas.delete(self.triangle_1_id)
        canvas.delete(self.triangle_2_id)

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        d1 = cursor_position.distance(self.start_point)
        d2 = cursor_position.distance(self.end_point)
        lineLen = self.start_point.distance(self.end_point)
        buffer = 0.2

        if d1 + d2 >= lineLen-buffer and d1 + d2 <= lineLen+buffer:
            return True
        
        return False

    def get_color(self) -> str:
        if self.is_selected:
            return self.selected_color
        elif self.is_path:
            return self.path_color
        elif self.is_dragged:
            return self.dragged_color
        else:
            return self.color
        
    def calculate_closest_edge_point(self, rect1_pos, rect1_width, rect1_height, rect2_pos, rect2_width, rect2_height):
        closest_point = Vector(0, 0)
        if rect1_pos.x + rect1_width < rect2_pos.x:
            closest_point.x = rect1_pos.x + rect1_width
        elif rect1_pos.x > rect2_pos.x + rect2_width:
            closest_point.x = rect1_pos.x
        else:
            closest_point.x = rect1_pos.x + rect1_width * 0.5

        if rect1_pos.y + rect1_height < rect2_pos.y:
            closest_point.y = rect1_pos.y + rect1_height
        elif rect1_pos.y > rect2_pos.y + rect2_height:
            closest_point.y = rect1_pos.y
        else:
            closest_point.y = rect1_pos.y + rect1_height * 0.5

        return closest_point

    def draw(self, canvas: tk.Canvas, tag: str = "edge"):
        # conncet nodes(rectangles) with line that touch thire closest edge
        closest_point1 = self.calculate_closest_edge_point(self.node1.position, self.node1.width, self.node1.height, self.node2.position, self.node2.width, self.node2.height)
        closest_point2 = self.calculate_closest_edge_point(self.node2.position, self.node2.width, self.node2.height, self.node1.position, self.node1.width, self.node1.height)

        # Draw the arrow to node2 
        if self.to_node1 == 1:
            arrow_points = self._calculate_arrow_points(closest_point1, closest_point2, 8)
            self.triangle_1_id = canvas.create_polygon(arrow_points, fill=self.get_color(), outline=self.get_color(), tags=tag)

        # Draw the arrow to node1
        if self.to_node2 == 1:
            arrow_points = self._calculate_arrow_points(closest_point2, closest_point1, 8)
            self.triangle_2_id = canvas.create_polygon(arrow_points, fill=self.get_color(), outline=self.get_color(), tags=tag)
            
        # Draw the line
        self.start_point.x = closest_point1.x
        self.start_point.y = closest_point1.y
        self.end_point.x = closest_point2.x
        self.end_point.y = closest_point2.y

        self.line_id = canvas.create_line(closest_point1.x, closest_point1.y, closest_point2.x, closest_point2.y, fill=self.get_color(), width=2, tags=tag)

    def _calculate_arrow_points(self, start_point: Vector, end_point: Vector, arrow_length: float) -> list[float]:
        if start_point.distance(end_point) < 40:
            return [0, 0, 0, 0, 0, 0]
        direction = (end_point - start_point).normalized()
        perpendicular = Vector(-direction.y, direction.x)
        arrow_points = [
            end_point.x, end_point.y,
            end_point.x - direction.x * arrow_length - perpendicular.x * arrow_length,
            end_point.y - direction.y * arrow_length - perpendicular.y * arrow_length,
            end_point.x - direction.x * arrow_length + perpendicular.x * arrow_length,
            end_point.y - direction.y * arrow_length + perpendicular.y * arrow_length
        ]
        return arrow_points

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Edge):
            return self.id == __value.id
        return False

    def __ne__(self, __value: object) -> bool:
        return self.__ne__(__value)