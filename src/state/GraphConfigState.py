from .State import State
from src.graph.GraphConfig import GraphConfig


class GraphConfigState(State):
    def __init__(self, initial_state: GraphConfig):
        super().__init__(initial_state)

    def set_number_of_nodes(self, number_of_nodes: int):
        self._state.number_of_nodes = number_of_nodes

        self.notify_subscribers()

    def set_probability(self, probability: float):
        self._state.probability = probability

        self.notify_subscribers()

    def set_is_show_intersections(self, is_show_intersections: bool):
        self._state.is_show_intersections = is_show_intersections

        self.notify_subscribers()

    def get_number_of_nodes(self) -> int:
        return self._state.number_of_nodes

    def get_probability(self) -> float:
        return self._state.probability

    def get_is_show_intersections(self) -> bool:
        return self._state.is_show_intersections


graph_config_state = GraphConfigState(GraphConfig())
