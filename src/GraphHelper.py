import numpy as np


class GraphHelper:
    @staticmethod
    def generateEmptyGraph(number_of_nodes):

        return np.arange(
            number_of_nodes * number_of_nodes).reshape((number_of_nodes, number_of_nodes))

    @staticmethod
    def get_matrix_string(matrix):
        # save matrix in a file
        matrix_string = ""
        for row in matrix:
            matrix_string += "| "
            for col in row:
                matrix_string += str(col) + " "
            matrix_string += "|\n"

        return matrix_string
