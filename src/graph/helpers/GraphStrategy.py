from src.graph.GraphModel import Graph, Tree, GraphModel, DirectedGraph
from abc import  abstractmethod

class Strategy:
    @abstractmethod
    def select(self) -> GraphModel:
        pass

class GraphStrategy(Strategy):
    def select(self) -> GraphModel:
        return Graph()
    
class TreeStrategy(Strategy):
    def select(self) -> GraphModel:
        return Tree()
    
class DirectedGraphStrategy(Strategy):
    def select(self) -> GraphModel:
        return DirectedGraph()

class GraphSelector:
    def set_graph_type(self, mode: str, is_directed: bool) -> "Strategy":
        if mode == "Graph" and not is_directed:
            return  GraphStrategy()
        elif mode == "Tree" and not is_directed:
            return TreeStrategy()
        elif mode == "Graph" and is_directed:
            return DirectedGraphStrategy()
        else:
            raise Exception("Invalid mode")
        
    def get_graph_type(self, mode: str, is_directed: bool) -> "GraphModel":
        return self.set_graph_type(mode, is_directed).select()