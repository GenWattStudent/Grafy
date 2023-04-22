import tkinter as tk
from copy import copy
from src.graph.GraphMatrix import GraphMatrix
from src.graph.elements.CanvasElement import CanvasElement
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.DrawHelper import DrawHelper
from src.graph.GraphConfig import GraphConfig
from src.layout.Kwaii import Kwaii
from src.utils.Event import Event
from src.graph.elements.Intersection import Intersection
from src.utils.Vector import Vector
from abc import abstractmethod
import random

class GraphModel:
    def __init__(self, config: GraphConfig = GraphConfig()):
        self.wages = GraphMatrix(config.number_of_nodes, float_type=True)
        self.matrix = GraphMatrix(config.number_of_nodes)
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.path: list[int] = []
        self.intersections: list[Intersection] = []
        self.selected_elements: list[CanvasElement] = []
        self.generator = DrawHelper()
        self.density = 0

        self.config = config
        self.prev_config: GraphConfig | None = None

        self.path_distance: float | None = None
        self.graph_change_event = Event()

    def clear(self):
        self.nodes = []
        self.edges = []
        self.intersections = []
        self.path = []
        self.path_distance = None
        self.set_number_of_nodes(self.config.number_of_nodes)

    def get_graph_elements(self):
        return self.nodes + self.edges + self.intersections

    def find_element_by_canvas_id(self, canvas_id: int) -> CanvasElement | None:
        for element in self.get_graph_elements():
            if element.canvas_id is not None and element.canvas_id == canvas_id:
                return element
        return None

    def get_nodes_from_list(self, elements: list[CanvasElement]) -> list[Node]:
        return [element for element in elements if isinstance(element, Node)]

    def get_edges_from_list(self, elements: list[CanvasElement]) -> list[Edge]:
        return [element for element in elements if isinstance(element, Edge)]

    def get_edges_connected_to_nodes(self, nodes: list[Node]) -> list[Edge]:
        edges = []
        for edge in self.edges:
            if edge.node1 in nodes or edge.node2 in nodes:
                edges.append(edge)
        return edges

    def delete(self, elements: list[CanvasElement]):
        elements = elements + self.get_edges_connected_to_nodes(self.get_nodes_from_list(elements))
        nodes = self.get_nodes_from_list(elements)
        edges = self.get_edges_from_list(elements)

        self.delete_edges(edges)
        self.delete_nodes(nodes)

    def delete_element(self, element: CanvasElement):
        if isinstance(element, Node):
            self.delete_node(element)
        elif isinstance(element, Edge):
            self.delete_edge(element)

    def add_element(self, element: CanvasElement):
        if isinstance(element, Node):
            self.add_node(element)
        elif isinstance(element, Edge):
            self.add_edge(element)

    def on_change(self, callback):
        self.graph_change_event += callback

    def off_change(self, callback):
        self.graph_change_event -= callback

    def get_wages(self) -> GraphMatrix:
        return self.wages

    def get_matrix(self) -> GraphMatrix:
        return self.matrix

    def get_graph_dictionary(self) -> dict[int, list[int]]:
        return self.matrix.get_graph_dictionary()

    def set_number_of_nodes(self, number_of_nodes: int):
        self.matrix.set_number_of_nodes(number_of_nodes)
        self.wages.set_number_of_nodes(number_of_nodes)

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.matrix.add_node()
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.density = self.calculate_density()

    def add_edge(self, edge: Edge):
        self.matrix.add_edge(edge)
        self.edges.append(edge)
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.density = self.calculate_density()

    def delete_node(self, node: Node):
        if node in self.nodes:
            self.matrix.delete_node(node.index - 1)
            self.nodes.remove(node)
            for node1 in self.nodes:
                if node1.index > node.index:
                    node1.index -= 1
            self.wages = self.generator.generate_wages(self, self.nodes)
            self.density = self.calculate_density()

    def delete_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.delete_node(node)

    def delete_edge(self, edge: Edge):
        # check if edge is in self.edges
        if edge in self.edges:
            self.matrix.delete_edge(edge)
            self.edges.remove(edge)
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.density = self.calculate_density()

    def delete_edges(self, edges: list[Edge]):
        for edge in edges:
            self.delete_edge(edge)

    def set_probability(self, probability: float):
        self.config.probability = probability
    
    def calculate_density(self) -> float:
        number_of_nodes = self.matrix.number_of_nodes
        return 2 * len(self.edges) / ((number_of_nodes * (number_of_nodes - 1)) + 0.0001)
    
    @abstractmethod
    def create(self, canvas: tk.Canvas):
        pass
    
    @abstractmethod
    def update(self, canvas: tk.Canvas, config: GraphConfig):
        pass

class Graph(GraphModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = Kwaii(self)

    def reset_graph(self, matrix: GraphMatrix):
        for i in range(matrix.number_of_nodes):
            for j in range(matrix.number_of_nodes):
                matrix[i][j] = 0
                
    def generate_graph_matrix(self) -> GraphMatrix:
        self.reset_graph(self.matrix)
        for i in range(self.matrix.number_of_nodes - 1):
            for j in range(i + 1, self.matrix.number_of_nodes):
                if random.random() < self.config.probability:
                    self.matrix[i][j] = 1
                    self.matrix[j][i] = 1

        return self.matrix
    
    def create(self, canvas: tk.Canvas):
        self.generate_graph_matrix()
        self.generator.selected_nodes.clear()
        self.nodes = self.generator.generate_nodes(self, 15, canvas.winfo_width(), canvas.winfo_height())
        self.layout.run()
        self.edges = self.generator.generate_edges(self.nodes, self)
        self.wages = self.generator.generate_wages(self, self.nodes)
        print(self.wages[0])
        self.density = self.calculate_density()

        return self.matrix
    
    def update(self, canvas: tk.Canvas, config: GraphConfig):
        if self.prev_config is None or self.matrix.number_of_nodes != config.number_of_nodes:
            self.set_number_of_nodes(config.number_of_nodes)
            self.create(canvas)
        if self.prev_config is None or self.prev_config.probability != config.probability:
            self.generate_graph_matrix()
            self.wages = self.generator.generate_wages(self, self.nodes)
            self.edges = self.generator.generate_edges(self.nodes, self)
            self.density = self.calculate_density()

        self.prev_config = copy(self.config)
        self.config = config
        self.graph_change_event(self)
        return self.matrix
    
class Tree(GraphModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def reset_graph(self, matrix: GraphMatrix):
        for i in range(matrix.number_of_nodes):
            for j in range(matrix.number_of_nodes):
                matrix[i][j] = 0

    def generate_tree_matrix(self) -> GraphMatrix:
        self.reset_graph(self.matrix)

        # Generate edges for tree structure
        for i in range(1, self.matrix.number_of_nodes):
            parent = (i - 1) // 2
            self.matrix[parent, i] = 1

        return self.matrix
    
    def generate_node_positions(self, matrix: GraphMatrix) -> list[Node]:
        nodes: list[Node] = []
        pos = {}
        n = matrix.number_of_nodes
        pos[0] = (n * 20, 20)
        nodes.append(Node(Vector(pos[0][0], pos[0][1]), 0, 15))
        for i in range(n):
            for j in range(n):
                if matrix[i, j] == 1:
                   pos[j] = (pos[i][0] + 20, pos[i][1] + 20)
                   nodes.append(Node(Vector(pos[i][0] + 20, pos[i][1] + 20),i, 15))
                    

        return nodes

    def create(self, canvas: tk.Canvas):
        self.generate_tree_matrix()
        self.nodes = self.generate_node_positions(self.matrix)
        self.generator.selected_nodes.clear()
        self.nodes = self.generator.generate_nodes(self, 15, canvas.winfo_width(), canvas.winfo_height())
        self.edges = self.generator.generate_edges(self.nodes, self)
        self.wages = self.generator.generate_wages(self, self.nodes)

        return self.matrix






