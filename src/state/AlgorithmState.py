from src.state.State import State
from enum import Enum


class SearchAlgorithmType(Enum):
    DIJKSTRA = "dijkstra"
    BFS = "bfs"
    DFS = "dfs"


class SearchAlgorithmData:
    def __init__(self, algorithm_name: SearchAlgorithmType, min_selected_nodes: int):
        self.algorithm_name = algorithm_name
        self.min_selected_nodes = min_selected_nodes


class BFSData(SearchAlgorithmData):
    def __init__(self):
        self.algorithm_name = SearchAlgorithmType.BFS
        self.min_selected_nodes: int = 1


class DFSData(SearchAlgorithmData):
    def __init__(self):
        self.algorithm_name = SearchAlgorithmType.DFS
        self.min_selected_nodes: int = 1


class DijkstraData(SearchAlgorithmData):
    def __init__(self):
        self.algorithm_name = SearchAlgorithmType.DIJKSTRA
        self.min_selected_nodes: int = 2


all_algorithms = [BFSData(), DFSData(), DijkstraData()]


class AlgorithmConfigState:
    def __init__(self,  search_algorithm: SearchAlgorithmData = BFSData()):
        self.search_algorithm = search_algorithm


class AlgorithmState(State):
    def __init__(self, initial_state: AlgorithmConfigState):
        super().__init__(initial_state)

    def set_search_algorithm(self, search_algorithm: str):
        # finds algorithm in list of all algorithm by name and set to state
        for algorithm in all_algorithms:
            if algorithm.algorithm_name.value == search_algorithm.lower():
                self._state.search_algorithm = algorithm
                break

        self.notify_subscribers()

    def get_search_algorithm(self) -> SearchAlgorithmData:
        return self._state.search_algorithm


algorithm_state = AlgorithmState(AlgorithmConfigState())
