import random
from src.graph.GraphMatrix import GraphMatrix
import src.constance as const


class Graph:
    def __init__(self, number_of_nodes=const.DEFAULT_NUMBER_OF_NODES, probability=const.DEFAULT_PROBABILITY):
        self.number_of_nodes = number_of_nodes
        self.probability = probability
        self.wages = GraphMatrix(number_of_nodes, float_type=True)
        self.matrix = GraphMatrix(number_of_nodes)

    def get_matrix(self) -> GraphMatrix:
        return self.matrix

    def get_graph_dictionary(self) -> dict[int, list[int]]:
        return self.matrix.get_graph_dictionary()

    def set_number_of_nodes(self, number_of_nodes: int):
        self.number_of_nodes = number_of_nodes
        self.matrix.set_number_of_nodes(number_of_nodes)
        self.wages.set_number_of_nodes(number_of_nodes)

    def set_probability(self, probability: float):
        self.probability = probability

    def reset_graph(self):
        for i in range(self.number_of_nodes):
            for j in range(self.number_of_nodes):
                self.matrix[i][j] = 0

    def generate_graph(self) -> GraphMatrix:
        self.reset_graph()
        for i in range(self.number_of_nodes - 1):
            for j in range(i + 1, self.number_of_nodes):
                if random.random() < self.probability:
                    self.matrix[i][j] = 1
                    self.matrix[j][i] = 1

        return self.matrix
