from ..Observable import Observable
from src.graph.GraphMatrix import GraphMatrix


class GraphSensor(Observable):
    def __init__(self):
        super().__init__()
        self._graph: GraphMatrix = None

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, value: GraphMatrix):
        self._graph = value
        self.notify_observers(value)


graph_state = GraphSensor()
