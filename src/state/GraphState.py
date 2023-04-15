from src.graph.GraphModel import GraphModel
from src.state.State import State


class GraphState(State):
    def __init__(self, initial_state: GraphModel | None = None):
        super().__init__(initial_state)


graph_state = GraphState()
