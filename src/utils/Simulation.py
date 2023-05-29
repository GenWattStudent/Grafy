from abc import ABC, abstractmethod
from src.graph.GraphModel import GraphModel
from src.graph.elements.Edge import Edge
from src.ui.GraphCanvas import GraphCanvas

class Simulation(ABC):
    def __init__(self):
        self.is_running = False

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def next(self):
        pass
    
    @abstractmethod
    def previous(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class PathSimulation(Simulation):
    def __init__(self, model: GraphModel, view: GraphCanvas):
        super().__init__()
        self.model = model
        self.ordered_edges: list[Edge] = []
        self.view = view
    
    def set_model(self, model: GraphModel):
        self.model = model

    def get_ordered_edges(self):
        self.ordered_edges.clear()
        if isinstance(self.model.path, dict):   
            for node1, neigbour in self.model.path.items():
                for node2 in neigbour:
                    for edge in self.model.edges:
                        if edge.node1.get_index() == node1 and edge.node2.get_index() == node2 or \
                                edge.node2.get_index() == node1 and edge.node1.get_index() == node2:
                            self.ordered_edges.append(edge)
                            break
    
    def set_not_path(self):
        for edge in self.model.edges:
            edge.is_path = False

    def set_path_back(self):
        for edge in self.ordered_edges:
            edge.is_path = True

    def next(self):
        for edge in self.ordered_edges:
            if edge.is_path == False:
                edge.is_path = True
                break
        
        self.view.draw_nodes_and_edges()
    
    def previous(self):
        for edge in reversed(self.ordered_edges):
            if edge.is_path == True:
                edge.is_path = False
                break
        self.view.draw_nodes_and_edges()

    def start(self):
        self.is_running = True
        self.get_ordered_edges()
        self.set_not_path()
        self.view.draw_nodes_and_edges()

    def stop(self):
        self.is_running = False
        self.set_path_back()
        self.view.draw_nodes_and_edges()