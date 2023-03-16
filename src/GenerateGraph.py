import random
from src.GraphHelper import GraphHelper


class Graph:
    def __init__(self, number_of_nodes=5, probability=0.1):
        self.number_of_nodes = number_of_nodes
        self.probability = probability
        self.graph = GraphHelper.generateEmptyGraph(number_of_nodes)

    def get_graph(self):
        return self.graph

    def set_number_of_nodes(self, number_of_nodes):
        self.number_of_nodes = number_of_nodes
        self.graph = GraphHelper.generateEmptyGraph(number_of_nodes)

    def set_probability(self, probability):
        self.probability = probability

    def reset_graph(self):
        for i in range(self.number_of_nodes):
            for j in range(self.number_of_nodes):
                self.graph[i][j] = 0

    def generate_graph(self):
        self.reset_graph()
        for i in range(self.number_of_nodes - 1):
            # crreate a loop that starts from i +1 to number_of_nodes

            for j in range(i + 1, self.number_of_nodes):
                if random.random() < self.probability:
                    self.graph[i][j] = 1
                    self.graph[j][i] = 1

        return self.graph

    def draw(self, graph):
        # print(self.graph)
        pass
