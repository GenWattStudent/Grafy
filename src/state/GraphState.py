from src.graph.Graph import Graph
from src.state.State import State


class GraphState(State):
    def __init__(self, initial_state: Graph | None = None):
        super().__init__(initial_state)


graph_state = GraphState()
