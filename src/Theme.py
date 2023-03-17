from src.graph.Node import Node
from src.graph.Edge import Edge


class Theme:
    def __init__(self, node_color: str, edge_color: str, node_dragged_color: str, edge_dragged_color: str):
        self.node_color = node_color
        self.node_dragged_color = node_dragged_color
        self.edge_color = edge_color
        self.edge_dragged_color = edge_dragged_color

    def get_node_color(self, node: Node):
        if node.is_dragged:
            return self.node_dragged_color
        else:
            return self.node_color

    def get_edge_color(self, edge: Edge):
        if edge.is_dragged:
            return self.edge_dragged_color
        else:
            return self.edge_color


theme = Theme("red", "white", "green", "yellow")
