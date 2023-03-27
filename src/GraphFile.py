import datetime
from src.graph.GraphHelper import GraphHelper
from src.graph.GraphMatrix import GraphMatrix
from abc import abstractmethod, ABC
import json


class FileManager(ABC):
    @abstractmethod
    def save(self, graph: GraphMatrix):
        pass

    @abstractmethod
    def load(self) -> GraphMatrix:
        pass


class GraphFile(FileManager):
    def __init__(self, path: str = ".", filename: str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")):
        self.path = path
        self.filename = filename
        self.rowToSkip: int = 3

    def save(self, graph: GraphMatrix):
        # save graph and students info in a file
        with open(self.path + "/" + self.filename, "w", encoding="utf-8") as txt_file:
            txt_file.write("Autorzy: Raszka Adrian, Jurzak Jakub, Lasota Kubuś" + "\n")
            txt_file.write("Grupa 2a, Informatyka dzienne" + "\n")
            txt_file.write("Macierz:" + "\n")
            txt_file.write(str(graph))

            json.dump(graph.get_graph_dictionary(), txt_file, indent=4)

    def load(self) -> GraphMatrix:
        # load graph and students info from a file
        with open(self.path + "/" + self.filename, "r") as txt_file:
            lines = txt_file.readlines()
            graph = GraphHelper().generate_empty_graph(len(lines) - self.rowToSkip)

            for i, line in enumerate(lines):
                if i <= self.rowToSkip - 1:
                    continue
                # take only numbers from line
                count = 0
                for number in enumerate(line):
                    if number[1].isdigit():
                        graph[i - self.rowToSkip][count] = int(number[1])
                        count += 1

            matrix = GraphMatrix(len(lines) - self.rowToSkip)
            matrix.set_matrix(graph)
            return  matrix
