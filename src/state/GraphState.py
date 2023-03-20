from src.graph.GraphMatrix import GraphMatrix
from src.state.State import State


class GraphState(State):
    def __init__(self, initial_state: GraphMatrix | None = None):
        super().__init__(initial_state)


graph_state = GraphState()
