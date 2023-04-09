import tkinter as tk
from copy import copy
from src.graph.GraphMatrix import GraphMatrix
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.DrawHelper import DrawHelper
from src.graph.GraphConfig import GraphConfig
from src.GraphFile import FileManager
from src.layout.Kwaii import Kwaii
from src.utils.Event import Event
from src.graph.elements.Intersection import Intersection
from src.ui.Toolbar import ToolBar
import random


class Graph:
    def __init__(
            self, file_manager: FileManager | None = None, config: GraphConfig = GraphConfig(),
            toolbar: ToolBar | None = None,):
        self.wages = GraphMatrix(config.number_of_nodes, float_type=True)
        self.matrix = GraphMatrix(config.number_of_nodes)
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.path: list[int] = []
        self.intersections: list[Intersection] = []
        self.selected_elements: list[Node | Edge | Intersection] = []
        self.generator = DrawHelper()
        self.toolbar = toolbar
        self.density = 0
        self.file_manager = file_manager
        self.config = config
        self.prev_config: GraphConfig | None = None
        self.layout = Kwaii(self)
        self.path_distance: float | None = None

        self.graph_change_event = Event()

    def get_graph_elements(self):
        return self.nodes + self.edges + self.intersections

    def find_element_by_canvas_id(self, canvas_id: int) -> Node | Edge | Intersection | None:
        for element in self.get_graph_elements():
            if element.canvas_id is not None and element.canvas_id == canvas_id:
                return element
        return None

    def select(self, element: Node | Edge | Intersection):
        if element not in self.selected_elements:
            element.is_selected = True
            self.selected_elements.append(element)
            self.graph_change_event()
        else:
            element.is_selected = False
            self.selected_elements.remove(element)
            self.graph_change_event()

    def deselect(self):
        for element in self.selected_elements:
            element.is_selected = False
        self.selected_elements.clear()
        self.graph_change_event()

    def get_nodes_from_list(self, elements: list[Node | Edge | Intersection]) -> list[Node]:
        return [element for element in elements if isinstance(element, Node)]

    def get_edges_from_list(self, elements: list[Node | Edge | Intersection]) -> list[Edge]:
        return [element for element in elements if isinstance(element, Edge)]

    def get_edges_connected_to_nodes(self, nodes: list[Node]) -> list[Edge]:
        edges = []
        for edge in self.edges:
            if edge.node1 in nodes or edge.node2 in nodes:
                edges.append(edge)
        return edges

    def delete(self, elements: list[Node | Edge | Intersection]):
        elements = elements + self.get_edges_connected_to_nodes(self.get_nodes_from_list(elements))
        nodes = self.get_nodes_from_list(elements)
        edges = self.get_edges_from_list(elements)

        self.delete_edges(edges)
        self.delete_nodes(nodes)

    def delete_selected(self):
        self.delete(self.selected_elements)
        self.selected_elements.clear()
        self.graph_change_event()

    def is_toolbar(self):
        return self.toolbar is not None

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

    def calculate_density(self) -> float:
        if self.config.number_of_nodes > 1:
            return 2 * len(self.edges) / (self.config.number_of_nodes * (self.config.number_of_nodes - 1))
        else:
            return 0

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

    def add_edge(self, edge: Edge):
        self.matrix.add_edge(edge)
        self.edges.append(edge)
        self.wages = self.generator.generate_wages(self, self.nodes)

    def delete_node(self, node: Node):
        if node in self.nodes:
            self.matrix.delete_node(node.index - 1)
            self.nodes.remove(node)
            for node1 in self.nodes:
                if node1.index > node.index:
                    node1.index -= 1
            self.wages = self.generator.generate_wages(self, self.nodes)

    def delete_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.delete_node(node)

    def delete_edge(self, edge: Edge):
        # check if edge is in self.edges
        if edge in self.edges:
            self.matrix.delete_edge(edge)
            self.edges.remove(edge)

    def delete_edges(self, edges: list[Edge]):
        for edge in edges:
            self.delete_edge(edge)

    def create(self, canvas: tk.Canvas) -> GraphMatrix:
        self.generate_graph_matrix()
        self.generator.selected_nodes.clear()
        self.nodes = self.generator.generate_nodes(self, 15, canvas.winfo_width(), canvas.winfo_height())
        self.edges = self.generator.generate_edges(self.nodes, self)
        self.wages = self.generator.generate_wages(self, self.nodes)
        self.density = self.calculate_density()
        self.layout.run()
        return self.matrix

    def update(self, config: GraphConfig, canvas: tk.Canvas) -> GraphMatrix:
        if self.prev_config is None or self.prev_config.number_of_nodes != config.number_of_nodes:
            self.set_number_of_nodes(config.number_of_nodes)
            self.create(canvas)
        if self.prev_config is None or self.prev_config.probability != config.probability:
            self.generate_graph_matrix()
            self.wages = self.generator.generate_wages(self, self.nodes)
            self.edges = self.generator.generate_edges(self.nodes, self)
            self.density = self.calculate_density()

        self.graph_change_event(self)
        self.prev_config = copy(self.config)
        self.config = config
        return self.matrix

    def set_probability(self, probability: float):
        self.config.probability = probability

    def reset_graph(self):
        for i in range(self.matrix.number_of_nodes):
            for j in range(self.matrix.number_of_nodes):
                self.matrix[i][j] = 0

    def generate_graph_matrix(self) -> GraphMatrix:
        self.reset_graph()
        for i in range(self.matrix.number_of_nodes - 1):
            for j in range(i + 1, self.matrix.number_of_nodes):
                if random.random() < self.config.probability:
                    self.matrix[i][j] = 1
                    self.matrix[j][i] = 1
        self.save_matrix()
        return self.matrix
