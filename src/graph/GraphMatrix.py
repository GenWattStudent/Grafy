from src.graph.GraphHelper import GraphHelper
import numpy as np


class GraphMatrix:
    def __init__(self, size: int):
        self.number_of_nodes = size
        self.matrix = GraphHelper.generateEmptyGraph(size)

    def get_matrix_string(self):
        return GraphHelper.get_matrix_string(self.matrix)

    def set_number_of_nodes(self, number_of_nodes: int):
        self.number_of_nodes = number_of_nodes
        self.reset_matrix()

    def get_matrix(self) -> np.ndarray[int, np.dtype[np.int64]]:
        return self.matrix

    def __str__(self) -> str:
        return self.get_matrix_string()

    def reset_matrix(self):
        self.matrix = GraphHelper.generateEmptyGraph(self.number_of_nodes)

    def __getitem__(self, item):
        return self.matrix[item]

    def __setitem__(self, key, value):
        self.matrix[key] = value
