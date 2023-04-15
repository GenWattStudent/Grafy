import tkinter as tk
from copy import copy
from src.graph.GraphMatrix import GraphMatrix
from src.graph.elements.CanvasElement import CanvasElement
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.DrawHelper import DrawHelper
from src.graph.GraphConfig import GraphConfig
from src.GraphFile import FileManager
from src.layout.Kwaii import Kwaii
from src.utils.Event import Event
from src.graph.elements.Intersection import Intersection
from src.utils.Vector import Vector
import random


class Graph:
    def __init__(self, graph_model: "GraphModel"):
        self.graph_model = graph_model
        self.matrix = graph_model.matrix
        self.density = 0
        self.layout = Kwaii(graph_model)

    def reset_graph(self, matrix: GraphMatrix):
        for i in range(matrix.number_of_nodes):
            for j in range(matrix.number_of_nodes):
                matrix[i][j] = 0

    def calculate_density(self) -> float:
        number_of_nodes = self.matrix.number_of_nodes
        return 2 * len(self.graph_model.edges) / ((number_of_nodes * (number_of_nodes - 1)) + 0.0001)
                
    def generate_graph_matrix(self) -> GraphMatrix:
        self.reset_graph(self.graph_model.matrix)
        for i in range(self.graph_model.matrix.number_of_nodes - 1):
            for j in range(i + 1, self.graph_model.matrix.number_of_nodes):
                if random.random() < self.graph_model.config.probability:
                    self.graph_model.matrix[i][j] = 1
                    self.graph_model.matrix[j][i] = 1

        return self.graph_model.matrix
    
    def create(self, canvas: tk.Canvas):
        self.generate_graph_matrix()
        self.graph_model.generator.selected_nodes.clear()
        self.graph_model.nodes = self.graph_model.generator.generate_nodes(self.graph_model, 15, canvas.winfo_width(), canvas.winfo_height())
        self.graph_model.edges = self.graph_model.generator.generate_edges(self.graph_model.nodes, self.graph_model)
        self.graph_model.wages = self.graph_model.generator.generate_wages(self.graph_model, self.graph_model.nodes)
        self.density = self.calculate_density()
        self.layout.run()
        return self.graph_model.matrix
    
    def update(self, canvas: tk.Canvas, config: GraphConfig):
        if self.graph_model.prev_config is None or self.graph_model.matrix.number_of_nodes != config.number_of_nodes:
            self.graph_model.set_number_of_nodes(config.number_of_nodes)
            self.create(canvas)
        if self.graph_model.prev_config is None or self.graph_model.prev_config.probability != config.probability:
            self.generate_graph_matrix()
            self.graph_model.wages = self.graph_model.generator.generate_wages(self.graph_model, self.graph_model.nodes)
            self.graph_model.edges = self.graph_model.generator.generate_edges(self.graph_model.nodes, self.graph_model)
            self.density = self.calculate_density()

        self.graph_model.prev_config = copy(self.graph_model.config)
        self.graph_model.config = config
        self.graph_model.graph_change_event(self.graph_model)
        return self.matrix
    
class Tree:
    def __init__(self, graph_model: "GraphModel"):
        self.graph_model = graph_model
        self.matrix = graph_model.matrix

    def reset_graph(self, matrix: GraphMatrix):
        for i in range(matrix.number_of_nodes):
            for j in range(matrix.number_of_nodes):
                matrix[i][j] = 0

    def generate_tree_matrix(self) -> GraphMatrix:
        self.reset_graph(self.graph_model.matrix)

        # Generate edges for tree structure
        for i in range(1, self.graph_model.matrix.number_of_nodes):
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
        self.graph_model.generator.selected_nodes.clear()
        self.graph_model.nodes = self.graph_model.generator.generate_nodes(self.graph_model, 15, canvas.winfo_width(), canvas.winfo_height())
        self.graph_model.edges = self.graph_model.generator.generate_edges(self.graph_model.nodes, self.graph_model)
        self.graph_model.wages = self.graph_model.generator.generate_wages(self.graph_model, self.graph_model.nodes)

        return self.graph_model.matrix

class GraphModel:
    def __init__(self, file_manager: FileManager | None = None, config: GraphConfig = GraphConfig()):
        self.wages = GraphMatrix(config.number_of_nodes, float_type=True)
        self.matrix = GraphMatrix(config.number_of_nodes)
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.path: list[int] = []
        self.intersections: list[Intersection] = []
        self.selected_elements: list[CanvasElement] = []
        self.generator = DrawHelper()

        self.file_manager = file_manager
        self.config = config
        self.prev_config: GraphConfig | None = None

        self.path_distance: float | None = None
        self.graph = Graph(self)
        self.tree = Tree(self)

        self.graph_change_event = Event()

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

    def save_matrix(self):
        if self.file_manager is not None:
            self.file_manager.save(self)

    def add_node(self, node: Node):
        self.nodes.append(node)
        self.matrix.add_node()
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.graph.density = self.graph.calculate_density()

    def add_edge(self, edge: Edge):
        self.matrix.add_edge(edge)
        self.edges.append(edge)
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.graph.density = self.graph.calculate_density()

    def delete_node(self, node: Node):
        if node in self.nodes:
            self.matrix.delete_node(node.index - 1)
            self.nodes.remove(node)
            for node1 in self.nodes:
                if node1.index > node.index:
                    node1.index -= 1
            self.wages = self.generator.generate_wages(self, self.nodes)
            self.graph.density = self.graph.calculate_density()

    def delete_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.delete_node(node)

    def delete_edge(self, edge: Edge):
        # check if edge is in self.edges
        if edge in self.edges:
            self.matrix.delete_edge(edge)
            self.edges.remove(edge)
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.graph.density = self.graph.calculate_density()

    def delete_edges(self, edges: list[Edge]):
        for edge in edges:
            self.delete_edge(edge)

    def create(self, canvas: tk.Canvas) -> GraphMatrix:
        return self.graph.create(canvas)

    def update(self, config: GraphConfig, canvas: tk.Canvas) -> GraphMatrix:
        return self.graph.update(canvas, config)

    def set_probability(self, probability: float):
        self.config.probability = probability




