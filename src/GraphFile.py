from __future__ import annotations

import datetime
from io import TextIOWrapper
from src.graph.GraphHelper import GraphHelper
from src.graph.GraphMatrix import GraphMatrix
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.Graph import Graph
from abc import abstractmethod, ABC
from src.algorithms.SearchAlgorithms import SearchAlgorithms
from src.state.AlgorithmState import algorithm_state


class FileManager(ABC):
    @abstractmethod
    def save(self, graph: Graph):
        pass

    @abstractmethod
    def load(self) -> GraphMatrix:
        pass


class GraphFile(FileManager):
    def __init__(self, path: str = ".", filename: str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")):
        self.path = path
        self.filename = filename
        self.rowToSkip: int = 3

    def save(self, graph: Graph):
        # save graph and students info in a file
        with open(self.path + "/" + self.filename, "w", encoding="utf-8") as txt_file:
            txt_file.write("Autorzy: Raszka Adrian, Jurzak Jakub, Lasota Kubuś" + "\n")
            txt_file.write("Grupa 2a, Informatyka dzienne" + "\n")
            txt_file.write("Macierz:" + "\n")
            txt_file.write(str(graph.get_matrix()) + "\n")
            txt_file.write("Słownik sąsiedztwa:" + "\n\n")

            dict = graph.get_graph_dictionary()
            self.write_dict(txt_file, dict)
            txt_file.write("\n")
            if len(
                    graph.generator.selected_nodes) > 0 and len(
                    graph.generator.selected_nodes) == algorithm_state.get_search_algorithm().min_selected_nodes:

                txt_file.write("BFS: " + "\n\n")
                bfs_dict = SearchAlgorithms().bfs(dict, graph.generator.selected_nodes[0])
                self.write_dict(txt_file, bfs_dict)

    def write_dict(self, txt_file: TextIOWrapper, dict:  dict[int, list[int]]):
        dict_array = str(dict).replace("{", "").replace("}", "").split("],")

        for i, line in enumerate(dict_array):
            if i != len(dict_array) - 1:
                txt_file.write((line + "],\n").replace(" ", ""))
            else:
                txt_file.write((line + ",\n").replace(" ", ""))

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
            return matrix
