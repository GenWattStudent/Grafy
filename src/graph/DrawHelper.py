from __future__ import annotations

from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.GraphHelper import GraphHelper
from src.utils.Vector import Vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphModel import GraphModel
from src.algorithms.SearchAlgorithms import SearchAlgorithms
from src.graph.GraphMatrix import GraphMatrix
from src.algorithms.Intersection import FindIntersection
from src.state.AlgorithmState import SearchAlgorithmType, algorithm_state
from src.Theme import theme
from src.graph.DrawGraphConfig import DrawGraphConfig

class DrawHelper:
    def __init__(self):
        self.search_algorithms = SearchAlgorithms()
        self.intersection = FindIntersection()
        self.selected_nodes: list[Node] = []
        self.draw_config = DrawGraphConfig()
        self.y_margin: int = 60

    def setup_graph(self, graph: GraphModel, max_width: float, max_height: float) -> tuple[list[Node], list[Edge]]:
        nodes = self.generate_nodes(graph, max_width, max_height)
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
            self, graph: GraphModel, nodes: list[Node],
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

    def generate_random_node(self, node_id: int, width: int, height: int, max_width: float, max_height: float) -> Node:
        max_x: float = max_width - width
        max_y: float = max_height - width
        min_x: float = width
        min_y: float = width
        vector: Vector = Vector().random(min_x, max_x, min_y+self.y_margin, max_y)

        return Node(vector, node_id, width, height)

    def generate_nodes(self, graph: GraphModel, max_width: float, max_height: float) -> list[Node]:
        nodes: list[Node] = []
        for i in range(graph.matrix.number_of_nodes):
            node: Node = self.generate_random_node(i + 1, self.draw_config.node_width, self.draw_config.node_height, max_width, max_height)
            j = 0
            while j < 100 and GraphHelper.check_rect_overlap(node.position.x, node.position.y, node.width, node.height, nodes):
                node: Node = self.generate_random_node(i + 1, self.draw_config.node_width, self.draw_config.node_height, max_width, max_height)
                j += 1

            nodes.append(node)

        return nodes

    def generate_edges(self, nodes: list[Node], graph: GraphModel) -> list[Edge]:
        edges: list[Edge] = []
        for i in range(graph.matrix.number_of_nodes - 1):
            for j in range(i + 1, graph.matrix.number_of_nodes):
                if graph.get_matrix()[i][j] == 1:
                    # calculate distance between nodes
                    distance: float = nodes[i].position.distance(nodes[j].position)
                    edge = Edge(nodes[i], nodes[j], distance, theme.get("fg"), graph.get_matrix()[i][j], graph.get_matrix()[j][i])
                    edges.append(edge)

        return edges

    def generate_wages(self, graph: GraphModel, nodes: list[Node]) -> GraphMatrix:
        if len(nodes) == 1:
            return GraphMatrix(0, float_type=True)
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

    def reset_edges_path(self, edges: list[Edge]):
        for edge in edges:
            edge.is_path = False

    def set_dragged_edges(self, edges: list[Edge], node: Node, value: bool = True):
        for edge in edges:
            if edge.node1 == node or edge.node2 == node:
                edge.is_dragged = value
