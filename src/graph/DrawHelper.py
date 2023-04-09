from __future__ import annotations

from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.GraphHelper import GraphHelper
from src.utils.Vector import Vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.Graph import Graph
from src.algorithms.SearchAlgorithms import SearchAlgorithms
from src.graph.GraphMatrix import GraphMatrix
from src.algorithms.Intersection import FindIntersection
from src.state.AlgorithmState import SearchAlgorithmType, algorithm_state
import customtkinter as ctk
from src.Theme import Theme


class DrawHelper:
    def __init__(self):
        self.search_algorithms = SearchAlgorithms()
        self.intersection = FindIntersection()
        self.selected_nodes: list[Node] = []
        self.y_margin: int = 60

    def setup_graph(self, graph: Graph, radius: int,
                    max_width: float, max_height: float) -> tuple[list[Node], list[Edge]]:
        nodes = self.generate_nodes(graph, radius, max_width, max_height)
        edges = self.generate_edges(nodes, graph)

        return nodes, edges

    def unselect_nodes(self):
        for node in self.selected_nodes:
            node.is_selected = False
        self.selected_nodes = []

    def select_nodes(self, node: Node):
        if len(self.selected_nodes) < algorithm_state.get_search_algorithm().min_selected_nodes:
            self.selected_nodes.append(node)
            node.is_selected = True
        else:
            self.unselect_nodes()
            self.selected_nodes.append(node)
            node.is_selected = True

    def search_best_path(
            self, graph: Graph, nodes: list[Node],
            selected_nodes: list[Node], algoritmType=SearchAlgorithmType.DIJKSTRA) -> tuple[float | None, list[int] | dict[int, list[int]]]:
        results: list[int] | dict[int, list[int]] = []
        lowest_distance: float | None = None

        if algoritmType == SearchAlgorithmType.DIJKSTRA:
            distance, path = self.search_algorithms.dijkstra(graph.wages, selected_nodes[0], selected_nodes[1])
            results = path
            lowest_distance = round(distance, 2)

        elif algoritmType == SearchAlgorithmType.BFS:
            path = self.search_algorithms.bfs(graph.get_graph_dictionary(), selected_nodes[0])
            results = path

        elif algoritmType == SearchAlgorithmType.DFS:
            path = self.search_algorithms.dfs(graph.get_graph_dictionary(), selected_nodes[0])
            results = path

        return lowest_distance, results

    def generate_random_node(self, node_id: int, radius: int, max_width: float, max_height: float) -> Node:
        max_x: float = max_width - radius
        max_y: float = max_height - radius
        vector: Vector = Vector().random(radius, max_x, radius+self.y_margin, max_y)

        return Node(
            vector, node_id, radius, Theme.get("node_color"),
            Theme.get("node_selected_color"),
            Theme.get("text_color"))

    def generate_nodes(self, graph: Graph, radius: int, max_width: float, max_height: float) -> list[Node]:
        nodes: list[Node] = []
        for i in range(graph.config.number_of_nodes):
            node: Node = self.generate_random_node(i + 1, radius, max_width, max_height)
            j = 0
            while j < 100 and GraphHelper.check_circle_overlap(
                    node.position.x, node.position.y, node.radius, nodes):
                node: Node = self.generate_random_node(i + 1, radius, max_width, max_height)
                j += 1

            nodes.append(node)

        return nodes

    def generate_edges(self, nodes: list[Node], graph: Graph) -> list[Edge]:
        edges: list[Edge] = []
        for i in range(graph.matrix.number_of_nodes - 1):
            for j in range(i + 1, graph.matrix.number_of_nodes):
                if graph.get_matrix()[i][j] == 1:
                    # calculate distance between nodes
                    distance: float = nodes[i].position.distance(nodes[j].position)
                    graph.wages[i][j] = distance
                    graph.wages[j][i] = distance
                    edge = Edge(nodes[i], nodes[j], distance, Theme.get("edge_color"))
                    edges.append(edge)

        return edges

    def generate_wages(self, graph: Graph, nodes: list[Node]) -> GraphMatrix:
        wages = GraphMatrix(graph.matrix.number_of_nodes, float_type=True)
        GraphHelper.fill_matrix_with_infinity(wages)

        for i in range(graph.matrix.number_of_nodes - 1):
            for j in range(i + 1, graph.matrix.number_of_nodes):
                if graph.get_matrix()[i][j] == 1:
                    # calculate distance between nodes
                    distance: float = nodes[i].position.distance(nodes[j].position)
                    wages[i][j] = round(distance, 1)
                    wages[j][i] = round(distance, 1)
        return wages

    def get_node_oval_position(self, node: Node) -> tuple[float, float, float, float]:
        return node.position.x - node.radius, node.position.y - node.radius, \
            node.position.x + node.radius, node.position.y + node.radius

    def reset_edges_path(self, edges: list[Edge]):
        for edge in edges:
            edge.is_path = False

    def set_dragged_edges(self, edges: list[Edge], node: Node, value: bool = True):
        for edge in edges:
            if edge.node1 == node or edge.node2 == node:
                edge.is_dragged = value
