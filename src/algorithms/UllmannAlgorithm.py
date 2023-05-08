from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphModel import GraphModel
class UllmannAlgorithm:
    def __init__(self, graph1: GraphModel, graph2: GraphModel):
        self.graph1 = graph1
        self.graph2 = graph2
        # matrix of graph1 and graph2
        self.matrix1 = graph1.matrix.get_matrix()
        self.matrix2 = graph2.matrix.get_matrix()
        # number of vertices in graph1 and graph2
        self.n1 = graph1.matrix.number_of_nodes
        self.n2 = graph2.matrix.number_of_nodes
        self.mapping = {}

    def is_isomorphic(self) -> bool:
        if self.n1 != self.n2:
            return False  

        return self.backtrack(0)

    def backtrack(self, u):
        if u == self.n1:
            return self.is_mapping_valid()

        for v in range(self.n2):
            if v not in self.mapping.values() and self.is_feasible(u, v):
                self.mapping[u] = v

                if self.backtrack(u + 1):
                    return True

                del self.mapping[u]

        return False

    def is_mapping_valid(self):
        for u1, v1 in self.mapping.items():
            for u2, v2 in self.mapping.items():
                if self.graph1.matrix[u1][u2] != self.graph2.matrix[v1][v2]:
                    return False

        return True

    def is_feasible(self, u, v):
        for u2 in range(self.n1):
            if self.graph1.matrix[u][u2] and u2 in self.mapping and not self.graph2.matrix[v][self.mapping[u2]]:
                return False

        return True