from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphModel import GraphModel
from src.utils.Vector import Vector
from src.layout.layout import Layout


class Kwaii(Layout):
    def __init__(self, graph: GraphModel):
        self.graph = graph
        self.repulsion_force_constant = 9000
        self.attraction_force_constant = 0.3
        self.damping_constant = 0.1
        self.time_step = 0.1
        self.iterations = 200

    def layout(self) -> GraphModel:
        for i in range(self.iterations):
            self.update_positions()
        return self.graph

    def update_positions(self) -> None:
    # Update edge distances
        for edge in self.graph.edges:
            edge.distance = abs(edge.node1.position - edge.node2.position)

        # Calculate repulsive forces
        repulsive_forces = [Vector() for _ in range(len(self.graph.nodes))]
        for i, node1 in enumerate(self.graph.nodes):
            for j, node2 in enumerate(self.graph.nodes[i + 1:], i + 1):
                force = self.repulsive_force(node1.position, node2.position, node1.radius, node2.radius)
                repulsive_forces[i] -= force
                repulsive_forces[j] += force

        # Calculate attractive forces
        attractive_forces = [Vector() for _ in range(len(self.graph.nodes))]
        for edge in self.graph.edges:
            if edge.distance is None:
                edge.distance = abs(edge.node1.position - edge.node2.position)
            force = self.attraction_force(edge.node1.position, edge.node2.position, edge.distance)
            attractive_forces[edge.node1.get_index()] += force
            attractive_forces[edge.node2.get_index()] -= force

        # Apply forces to nodes
        for i, node in enumerate(self.graph.nodes):
            net_force = repulsive_forces[i] + attractive_forces[i]
            node.position += self.damping_constant * net_force * self.time_step

    def repulsive_force(self, pos1: Vector, pos2: Vector, r1: int, r2: int) -> Vector:
        delta = pos1 - pos2
        distance = abs(delta)
        if distance == 0:
            return Vector()
        direction = delta.normalized()
        magnitude = self.repulsion_force_constant * r1 * r2 / (distance * distance)
        return magnitude * direction

    def attraction_force(self, pos1: Vector, pos2: Vector, length: float) -> Vector:
        delta = pos2 - pos1
        direction = delta.normalized()
        distance = abs(delta)
        magnitude = self.attraction_force_constant * (distance - length)
        return magnitude * direction
