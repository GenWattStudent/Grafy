import random
import customtkinter as ctk
from copy import copy
from src.graph.GraphMatrix import GraphMatrix
from src.graph.Node import Node
from src.graph.Edge import Edge
from src.graph.DrawHelper import DrawHelper
from src.graph.GraphConfig import GraphConfig
from src.layout.Kwaii import Kwaii


class Graph:
    def __init__(self, config: GraphConfig = GraphConfig()):
        self.wages = GraphMatrix(config.number_of_nodes, float_type=True)
        self.matrix = GraphMatrix(config.number_of_nodes)
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.path: list[int] = []
        self.intersections: list[tuple[float, float]] = []
        self.generator = DrawHelper()
        self.config = config
        self.prev_config: GraphConfig | None = None
        self.layout = Kwaii(self)

    def get_matrix(self) -> GraphMatrix:
        return self.matrix

    def get_graph_dictionary(self) -> dict[int, list[int]]:
        return self.matrix.get_graph_dictionary()

    def set_number_of_nodes(self, number_of_nodes: int):
        self.matrix.set_number_of_nodes(number_of_nodes)
        self.wages.set_number_of_nodes(number_of_nodes)

    def create(self, canvas: ctk.CTkCanvas) -> GraphMatrix:
        self.generate_graph_matrix()
        self.generator.selected_nodes.clear()
        self.nodes = self.generator.generate_nodes(self, 15, canvas.winfo_width(), canvas.winfo_height())
        self.edges = self.generator.generate_edges(self.nodes, self)
        self.layout.run()
        return self.matrix

    def update(self, config: GraphConfig, canvas: ctk.CTkCanvas) -> GraphMatrix:
        if self.prev_config is None or self.prev_config.number_of_nodes != config.number_of_nodes:
            self.set_number_of_nodes(config.number_of_nodes)
            self.create(canvas)
        if self.prev_config is None or self.prev_config.probability != config.probability:
            self.generate_graph_matrix()
            self.edges = self.generator.generate_edges(self.nodes, self)

        self.prev_config = copy(self.config)
        self.config = config
        return self.matrix

    def set_probability(self, probability: float):
        self.config.probability = probability

    def reset_graph(self):
        for i in range(self.config.number_of_nodes):
            for j in range(self.config.number_of_nodes):
                self.matrix[i][j] = 0

    def generate_graph_matrix(self) -> GraphMatrix:
        self.reset_graph()
        for i in range(self.config.number_of_nodes - 1):
            for j in range(i + 1, self.config.number_of_nodes):
                if random.random() < self.config.probability:
                    self.matrix[i][j] = 1
                    self.matrix[j][i] = 1

        return self.matrix
