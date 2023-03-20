from src.ui.GraphCanvas import GraphCanvas
from src.graph.Graph import Graph


class DrawGraph(GraphCanvas):
    def __init__(self, master, graph: Graph):
        super().__init__(master, graph=graph)
        self.graph = graph

    def update_intersections(self):
        self.toggle_intersection()

    def update_probability(self):
        edges = self.draw_helper.generate_edges(self.nodes, self.graph)
        self.set_edges(edges)
        self.show_intersections()
        self.draw_edges(edges)
        self.draw_nodes(self.nodes)

    def update_number_of_nodes(self):
        self.draw_graph()
