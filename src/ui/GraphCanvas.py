import tkinter as tk
from src.graph.Graph import Graph
from src.utils.Vector import Vector
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.elements.Intersection import Intersection
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.state.AlgorithmState import algorithm_state
from src.state.GraphState import graph_state
from src.graph.helpers.CanvasHelper import CanvasHelper
from src.Theme import Theme
import math as math
import threading


class GraphCanvas(tk.Canvas):
    def __init__(self, master, graph: Graph, draw_config: DrawGraphConfig = DrawGraphConfig(), **kwargs):
        super().__init__(master, **kwargs)
        self.draw_config = draw_config

        self.is_intersection: bool = False
        self.draging_node = None
        self.canvas_elements = []

        self.graph: Graph = graph
        self.canvas_helper = CanvasHelper(self)

        self.configure(bg=Theme.get("canvas_bg_color"))
        self.configure(highlightthickness=0)
        self.config(scrollregion=self.bbox(tk.ALL))

    def toggle_intersection(self):
        self.is_intersection = not self.is_intersection
        if self.is_intersection:
            self.show_intersections()
        else:
            self.delete("intersection")

    def set_edges(self, edges: list[Edge]):
        self.graph.edges = edges

    def set_nodes(self, nodes: list[Node]):
        self.graph.nodes = nodes

    def change_cursor(self, event):
        # change cursor when mouse if over node
        x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
        for element in self.graph.get_graph_elements():
            if element.is_under_cursor(Vector(x, y)):
                return self.configure(cursor='hand1')

        self.configure(cursor='fleur')

    def reset_graph(self):
        self.graph.nodes.clear()
        self.graph.edges.clear()
        self.graph.intersections.clear()
        self.graph.generator.reset_edges_path(self.graph.edges)
        self.delete("all")

    def draw_path(self, path: list[int] | dict[int, list[int]]):
        self.graph.generator.reset_edges_path(self.graph.edges)

        # set is_path to true for all edges in path
        if isinstance(path, list):
            for i in range(len(path) - 1):
                for edge in self.graph.edges:
                    if edge.node1 == self.graph.nodes[path[i]] and edge.node2 == self.graph.nodes[path[i + 1]] or \
                            edge.node2 == self.graph.nodes[path[i]] and edge.node1 == self.graph.nodes[path[i + 1]]:
                        edge.is_path = True

        elif isinstance(path, dict):
            # draw path from dictionary
            for key, value in path.items():
                for edge in self.graph.edges:
                    if edge.node1.get_index() == key and edge.node2.get_index() in value or \
                            edge.node2.get_index() == key and edge.node1.get_index() in value:
                        edge.is_path = True

        self.draw_nodes_and_edges()

    def search_path(self) -> tuple[float | None, list[int] | dict[int, list[int]]] | None:
        selected_nodes = self.graph.get_nodes_from_list(self.graph.selected_elements)
        if algorithm_state.get_search_algorithm().min_selected_nodes == len(selected_nodes):
            distance, path = self.graph.generator.search_best_path(
                self.graph, self.graph.nodes, selected_nodes, algorithm_state.get_search_algorithm().algorithm_name)

            self.draw_path(path)
            self.graph.path_distance = distance
            graph_state.set(self.graph)
            return distance, path

    def draw_intersections(self, intersections: list[Intersection]):
        for intersection in intersections:
            intersection.draw(self)

    def setup_intersections(self):
        self.graph.intersections = self.graph.generator.intersection.find_intersections(self.graph.edges)

    def draw_graph(self):
        self.delete("all")
        self.draw_nodes_and_edges()
        self.show_intersections()

    def show_intersections(self):
        if self.is_intersection:
            self.setup_intersections()
            thread = threading.Thread(target=self.draw_intersections, args=(self.graph.intersections,))
            thread.daemon = True
            thread.start()

    def draw_nodes_and_edges(self):
        self.draw_edges(self.graph.edges)
        self.draw_nodes(self.graph.nodes)

    def draw_edges(self, edges: list[Edge]):
        self.delete("edge")
        for edge in edges:
            edge.draw(self)

    def draw_nodes(self, nodes: list[Node]):
        self.delete("node")
        for node in nodes:
            node.draw(self)
