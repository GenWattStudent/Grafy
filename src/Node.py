from src.utils.Vector import Vector


class Node:
    def __init__(self, index, position: Vector, radius=15):
        self.index = index
        self.position: Vector = position
        self.radius = radius
