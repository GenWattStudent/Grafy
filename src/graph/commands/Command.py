from abc import ABC, abstractmethod
from src.state.GraphState import graph_state
from src.graph.Graph import Graph
from src.graph.elements.Node import Node
from copy import copy


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class AddNodeCommand(Command):
    def __init__(self, graph_model: Graph, node: Node):
        self.graph_model = graph_model
        self.node = node

    def execute(self):
        self.graph_model.add_node(self.node)
        graph_state.set(self.graph_model)

    def undo(self):
        self.graph_model.delete_node(self.node)
        graph_state.set(self.graph_model)


class AddEdgeCommand(Command):
    def __init__(self, graph_model, edge):
        self.graph_model = graph_model
        self.edge = edge

    def execute(self):
        self.graph_model.add_edge(self.edge)
        graph_state.set(self.graph_model)

    def undo(self):
        self.graph_model.delete_edge(self.edge)
        graph_state.set(self.graph_model)


class DeleteElementCommand(Command):
    def __init__(self, graph_model, elements):
        self.graph_model = graph_model
        self.elements = copy(elements)

    def execute(self):
        for element in self.elements:
            self.graph_model.delete_element(element)
        graph_state.set(self.graph_model)

    def undo(self):
        for element in self.elements:
            self.graph_model.add_element(element)
        graph_state.set(self.graph_model)