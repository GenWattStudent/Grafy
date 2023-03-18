from src.utils.Vector import Vector


class Node:
    def __init__(self, position: Vector, index: str | int = "", radius: int = 15):
        self.index: str | int = index
        self.position: Vector = position
        self.radius: int = radius
        self.is_dragged: bool = False
        self.is_selected: bool = False

    def is_under_cursor(self, cursor_position: Vector) -> bool:
        return (self.position - cursor_position).length() <= self.radius

    def __str__(self):
        return f"Node({self.index}, {self.position}, {self.radius})"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.index == other.index

    def distance(self, other: "Node"):
        return (self.position - other.position).length()
