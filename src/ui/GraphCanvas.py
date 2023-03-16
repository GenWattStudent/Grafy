import customtkinter as ctk
from src.Graph import Graph
from src.utils.Vector import Vector
from src.Node import Node
from src.Edge import Edge


class GraphCanvas(ctk.CTkCanvas):
    def __init__(self, master, graph: Graph, **kwargs):
        super().__init__(master, **kwargs)
        self.graph: Graph = graph
        self.nodes = []
        self.edges = []
        self.configure(bg='#2b2b2b')

    def generate_nodes(self):
        for i in range(self.graph.number_of_nodes):
            node = Node(i + 1, Vector().random(0, 580, 0, 800))
            self.nodes.append(node)
        return self.nodes

    def generate_edges(self, nodes: list[Node], graph: list[list[int]], number_of_nodes: int):
        for i in range(number_of_nodes - 1):
            for j in range(i + 1, number_of_nodes):
                if graph[i][j] == 1:
                    edge = Edge(nodes[i], nodes[j])
                    self.edges.append(edge)
        return self.edges

    def reset_graph(self):
        self.nodes.clear()
        self.edges.clear()
        self.delete("all")

    def draw_graph(self):
        self.reset_graph()
        nodes: list[Node] = self.generate_nodes()
        edges: list[Edge] = self.generate_edges(nodes, self.graph.graph, self.graph.number_of_nodes)

        self.draw_edges(edges)
        self.draw_nodes(nodes)

    def draw_edges(self, edges: list[Edge]):
        for edge in edges:
            self.draw_edge(edge.node1, edge.node2)

    def draw_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.draw_node(node)

    def draw_node(self, node: Node):
        self.create_oval(node.position.x - node.radius, node.position.y - node.radius,
                         node.position.x + node.radius, node.position.y + node.radius, fill="red")
        self.create_text(node.position.x, node.position.y, text=str(node.index), fill="white")

    def draw_edge(self, node1: Node, node2: Node):
        self.create_line(node1.position.x, node1.position.y, node2.position.x, node2.position.y, fill="white")
