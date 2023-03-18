from src.graph.Node import Node


class Edge:
    def __init__(self, node1: Node, node2: Node, distance: float | None = None):
        self.node1 = node1
        self.node2 = node2
        self.is_dragged: bool = False
        self.is_path: bool = False
        self.distance = distance
