from src.graph.Node import Node


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2
        self.is_dragged: bool = False
