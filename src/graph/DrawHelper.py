from src.graph.Node import Node
from src.graph.Edge import Edge
from src.graph.GraphHelper import GraphHelper
from src.utils.Vector import Vector
from src.graph.Graph import Graph
from src.algorithms.SearchAlgorithms import SearchAlgorithms
from src.graph.GraphMatrix import GraphMatrix
from src.algorithms.Intersection import Intersection
import math
from enum import Enum


class SearchAlgorithmType(Enum):
    DIJKSTRA = "dijkstra"
    BFS = "bfs"
    A_STAR = "a_star"


class DrawHelper:
    def __init__(self):
        self.search_algorithms = SearchAlgorithms()
        self.intersection = Intersection()
        self.first_selected_node: Node | None = None
        self.second_selected_node: Node | None = None
        self.y_margin: int = 60

    def setup_graph(self, graph: Graph, radius: int,  edges: list[Edge],
                    max_width: float, max_height: float) -> tuple[list[Node], list[Edge]]:
        nodes = self.generate_nodes(graph, radius, max_width, max_height)
        edges = self.generate_edges(nodes, graph)

        return nodes, edges

    def unselect_nodes(self):
        if self.first_selected_node:
            self.first_selected_node.is_selected = False
        if self.second_selected_node:
            self.second_selected_node.is_selected = False
        self.first_selected_node = None
        self.second_selected_node = None

    def select_nodes(self, node: Node):
        if not self.first_selected_node:
            self.first_selected_node = node
            self.first_selected_node.is_selected = True
        elif not self.second_selected_node:
            self.second_selected_node = node
            self.second_selected_node.is_selected = True
        elif self.first_selected_node and self.second_selected_node:
            self.unselect_nodes()
            self.first_selected_node = node
            self.first_selected_node.is_selected = True

    def search_best_path(
            self, graph: Graph, nodes: list[Node],
            start_node: Node, end_node: Node, algoritmType=SearchAlgorithmType.DIJKSTRA) -> tuple[float, list[int]]:
        best_path: list[int] = []
        lowest_distance: float = math.inf

        if algoritmType == SearchAlgorithmType.DIJKSTRA:
            wages = self.generate_wages(graph, nodes)
            distance, path = self.search_algorithms.dijkstra(wages, start_node, end_node)
            best_path = path
            lowest_distance = distance

        elif algoritmType == SearchAlgorithmType.BFS:
            distance, path = self.search_algorithms.bfs(graph.get_graph(), start_node, end_node)
            best_path = path
            lowest_distance = distance

        return lowest_distance, best_path

    def generate_random_node(self, node_id: int, radius: int, max_width: float, max_height: float) -> Node:
        max_x: float = max_width - radius
        max_y: float = max_height - radius
        vector: Vector = Vector().random(radius, max_x, radius+self.y_margin, max_y)

        return Node(vector, node_id, radius)

    def generate_nodes(self, graph: Graph, radius: int, max_width: float, max_height: float) -> list[Node]:
        nodes: list[Node] = []
        for i in range(graph.number_of_nodes):
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
        for i in range(graph.number_of_nodes - 1):
            for j in range(i + 1, graph.number_of_nodes):
                if graph.get_graph()[i][j] == 1:
                    # calculate distance between nodes
                    distance: float = nodes[i].position.distance(nodes[j].position)
                    graph.wages[i][j] = distance
                    graph.wages[j][i] = distance
                    edge = Edge(nodes[i], nodes[j], distance)
                    edges.append(edge)

        return edges

    def generate_wages(self, graph: Graph, nodes: list[Node]) -> GraphMatrix:
        wages = GraphMatrix(graph.number_of_nodes, float_type=True)
        GraphHelper.fill_matrix_with_infinity(wages)

        for i in range(graph.number_of_nodes - 1):
            for j in range(i + 1, graph.number_of_nodes):
                if graph.get_graph()[i][j] == 1:
                    # calculate distance between nodes
                    distance: float = nodes[i].position.distance(nodes[j].position)
                    wages[i][j] = math.floor(distance)
                    wages[j][i] = math.floor(distance)
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
