import datetime
import string
from src.GraphHelper import GraphHelper


class ManageFiles:
    def __init__(self, path=".", filename: string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")):
        self.path = path
        self.filename = filename
        self.rowToSkip = 3

    def save_graph_with_students_info(self, graph):
        print(graph)
        # save graph and students info in a file
        with open(self.path + "/" + self.filename, "w") as txt_file:
            txt_file.write("Autorzy: Raszka Adrian, Jurzak Jakub, Lasota Kubuś" + "\n")
            txt_file.write("Grupa 2a, Informatyka dzienne" + "\n")
            txt_file.write("Macierz:" + "\n")
            txt_file.write(self.get_matrix_string(graph))

    def get_matrix_string(self, matrix):
        # save matrix in a file
        matrix_string = ""
        for row in matrix:
            matrix_string += "| "
            for col in row:
                matrix_string += str(col) + " "
            matrix_string += "|\n"

        return matrix_string

    def load_graph_with_students_info(self):
        # load graph and students info from a file
        with open(self.path + "/" + self.filename, "r") as txt_file:
            lines = txt_file.readlines()
            graph = GraphHelper().generateEmptyGraph(len(lines) - self.rowToSkip)

            for i, line in enumerate(lines):
                if i <= self.rowToSkip - 1:
                    continue
                # take only numbers from line
                count = 0
                for number in enumerate(line):
                    if number[1].isdigit():
                        graph[i - self.rowToSkip][count] = int(number[1])
                        count += 1

            return graph
