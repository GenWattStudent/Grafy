import numpy as np
from .Node import Node
import customtkinter as ctk


class GraphHelper:
    @staticmethod
    def generateEmptyGraph(number_of_nodes: int) -> np.ndarray[int, np.dtype[np.int64]]:
        return np.arange(
            number_of_nodes * number_of_nodes).reshape(number_of_nodes, number_of_nodes)

    @staticmethod
    def get_matrix_string(matrix: np.ndarray[int, np.dtype[np.int64]]):
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
