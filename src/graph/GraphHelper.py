import numpy as np
from src.graph.elements.Node import Node
import customtkinter as ctk


class GraphHelper:
    @staticmethod
    def generate_empty_graph(number_of_nodes: int):
        return np.arange(
            number_of_nodes * number_of_nodes, dtype=np.int8).reshape(number_of_nodes, number_of_nodes)

    @staticmethod
    def generate_empty_wages(number_of_nodes: int):
        return np.arange(
            number_of_nodes * number_of_nodes, dtype=np.float32).reshape(number_of_nodes, number_of_nodes)

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

    @staticmethod
    def is_circle_out_of_bounds(element: ctk.CTkCanvas, x: float, y: float, radius: int) -> bool:
        return x - radius < 0 or x + radius > element.winfo_width() or y - radius < 0 or y + radius > element.winfo_height()

    @staticmethod
    def get_matrix_as_dictionary(matrix) -> dict[int, list[float]]:
        dictionary = {}
        for i in range(len(matrix)):
            dictionary[i] = []
            for j in range(len(matrix[i])):
                if matrix[i][j] == 1:
                    dictionary[i].append(j)
        return dictionary

    @staticmethod
    def get_wages(nodes: list[Node]):
        wages = np.arange(len(nodes) * len(nodes)).reshape(len(nodes), len(nodes))
        for i in range(len(nodes) - 1):
            for j in range(i + 1, len(nodes)):
                distance: float = nodes[i].distance(nodes[j])
                wages[i][j] = distance
                wages[j][i] = distance
        return wages

    @staticmethod
    def fill_matrix_with_infinity(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = np.inf
