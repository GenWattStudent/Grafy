import numpy as np


class GraphHelper:
    @staticmethod
    def generateEmptyGraph(number_of_nodes):

        return np.arange(
            number_of_nodes * number_of_nodes).reshape((number_of_nodes, number_of_nodes))
