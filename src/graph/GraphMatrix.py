from src.graph.GraphHelper import GraphHelper
from numpy import ndarray, float32, dtype
from typing import Any


class GraphMatrix:
    def __init__(self, size: int, float_type: bool = False):
        self.number_of_nodes = size
        self.float_type = float_type
        self.matrix = self.generate_matrix_depends_on_type()

    def get_matrix_string(self):
        return GraphHelper.get_matrix_string(self.matrix)

    def set_matrix(self, matrix):
        self.matrix = matrix

    def get_graph_dictionary(self) -> dict[int, list[int]]:
        dict = {}
        for i in range(self.number_of_nodes):
            dict[i] = []
            for j in range(self.number_of_nodes):
                if self.matrix[i][j] == 1:
                    dict[i].append(j)
        return dict

    def generate_matrix_depends_on_type(self):
        if self.float_type:
            return GraphHelper.generate_empty_wages(self.number_of_nodes)

        return GraphHelper.generate_empty_graph(self.number_of_nodes)

    def set_number_of_nodes(self, number_of_nodes: int):
        self.number_of_nodes = number_of_nodes
        self.reset_matrix()

    def get_matrix(self):
        return self.matrix

    def __str__(self) -> str:
        return self.get_matrix_string()

    def reset_matrix(self):
        self.matrix = GraphHelper.generate_empty_graph(self.number_of_nodes)

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        self.matrix[key] = value

    def __len__(self):
        return len(self.matrix)
