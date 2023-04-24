from src.graph.GraphModel import Graph, Tree, GraphModel
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

class GraphSelector:
    def set_graph_type(self, mode: str) -> "Strategy":
        if mode == "Graph":
            return  GraphStrategy()
        elif mode == "Tree":
            return TreeStrategy()
        else:
            return GraphStrategy()
        
    def get_graph_type(self, mode: str) -> "GraphModel":
        return self.set_graph_type(mode).select()