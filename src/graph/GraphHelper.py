import numpy as np
from .Node import Node


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

    @staticmethod
    def check_circle_overlap(x: float, y: float, radius: int, circles: list[Node]):
        for circle in circles:
            x0 = circle.position.x
            y0 = circle.position.y
            r0 = circle.radius
            if ((x - x0)**2 + (y - y0)**2)**0.5 <= radius + r0:
                return True
        return False
