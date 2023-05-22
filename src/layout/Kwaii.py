from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphModel import GraphModel
from src.utils.Vector import Vector
from src.layout.layout import Layout


class Kwaii(Layout):
    def __init__(self, graph: GraphModel, area: float = 1000.0, k: float = 0.9, iterations: int = 50):
        self.graph = graph
        self.area = area
        self.k = k
        self.iterations = iterations

    def layout(self) -> GraphModel:
        # Initialize node positions randomly
        for node in self.graph.nodes:
            node.position = Vector().random(0, self.area, 0, self.area)

        # Perform iterations of the algorithm
        for i in range(self.iterations):
            # Calculate repulsive forces between nodes
            for node1 in self.graph.nodes:
                node1.disp = Vector()
                for node2 in self.graph.nodes:
                    if node1 != node2:
                        delta = node1.position - node2.position
                        distance = abs(delta)
                        if distance > 0:
                            direction = delta.normalized()
                            repulsive_force = self.k * self.k / distance
                            node1.disp += direction * repulsive_force

            # Calculate attractive forces between edges
            for edge in self.graph.edges:
                delta = edge.node1.position - edge.node2.position
                distance = abs(delta)
                if distance > 0:
                    direction = delta.normalized()
                    attractive_force = distance * distance / self.k
                    edge.node1.disp -= direction * attractive_force
                    edge.node2.disp += direction * attractive_force

            # Limit maximum displacement per iteration
            for node in self.graph.nodes:
                distance = abs(node.disp)
                if distance > 0:
                    direction = node.disp.normalized()
                    max_distance = min(distance, self.iterations)
                    node.position += direction * max_distance

        return self.graph

