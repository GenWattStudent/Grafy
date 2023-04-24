from __future__ import annotations

import datetime
from io import TextIOWrapper
from src.graph.GraphHelper import GraphHelper
from src.graph.GraphMatrix import GraphMatrix
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.graph.GraphModel import GraphModel
from abc import abstractmethod, ABC
from src.algorithms.SearchAlgorithms import SearchAlgorithms
from src.state.AlgorithmState import algorithm_state


class FileManager(ABC):
    @abstractmethod
    def save(self, graph: GraphModel, path: str):
        pass

    @abstractmethod
    def load(self, path: str) -> GraphModel:
        pass


class GraphFile(FileManager):
    def __init__(self, path: str = ".", filename: str = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")):
        self.path = path
        self.filename = filename
        self.rowToSkip: int = 3

    def save(self, graph: GraphModel, path: str):
        # save graph and students info in a file
        with open(self.path + "/" + self.filename, "w", encoding="utf-8") as txt_file:
            txt_file.write("Autorzy: Raszka Adrian, Jurzak Jakub, Lasota Kubuś" + "\n")
            txt_file.write("Grupa 2a, Informatyka dzienne" + "\n")
            txt_file.write("\nMacierz: \n\n")
            txt_file.write(str(graph.get_matrix()) + "\n")
            txt_file.write("Słownik sąsiedztwa:" + "\n\n")

            dict = graph.get_graph_dictionary()
            self.write_dict(txt_file, dict)
            selected_nodes = graph.get_nodes_from_list(graph.selected_elements)
            
            if len(selected_nodes) > 0 and len(
                    selected_nodes) == algorithm_state.get_search_algorithm().min_selected_nodes:
                
                search_algorithms = SearchAlgorithms()
                
                bfs_dict = search_algorithms.bfs(dict, selected_nodes[0])
                txt_file.write("\nBFS OUTPUT: " + "\n\n")
                self.write_dict(txt_file, bfs_dict)
                bfs_layers = search_algorithms.get_layers_from_bfs_output(bfs_dict, selected_nodes[0].index - 1)
                txt_file.write("\nBFS LAYERS: " + "\n\n")
                for layer, vertices in bfs_layers:
                    txt_file.write("Layer {}: {}".format(layer + 1, vertices) + "\n")

            sumCountDegree = len(graph.edges) * 2
            txt_file.write(f"\nSuma stopni: {sumCountDegree}")
            txt_file.write(f"\nLiczba krawedzi grafow: {int(0.5 * sumCountDegree)}")
            txt_file.write(f"\nGestosc grafu: {round(graph.density, 2)}")

    def write_dict(self, txt_file: TextIOWrapper, dict: dict[int, list[int]]):
        dict_array = str(dict).replace("{", "").replace("}", "").split("],")

        for i, line in enumerate(dict_array):
            if i != len(dict_array) - 1:
                txt_file.write((line + "],\n").replace(" ", ""))
            else:
                txt_file.write((line + ",\n").replace(" ", ""))

    def load(self, path: str) -> GraphModel:
        return GraphModel()