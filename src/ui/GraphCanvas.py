import customtkinter as ctk
from src.Theme import theme
from src.graph.Graph import Graph
from src.utils.Vector import Vector
from src.graph.Node import Node
from src.graph.Edge import Edge
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.state.AlgorithmState import algorithm_state
import math as math
import threading


class GraphCanvas(ctk.CTkCanvas):
    def __init__(self, master, graph: Graph, draw_config: DrawGraphConfig = DrawGraphConfig(), **kwargs):
        super().__init__(master, **kwargs)
        self.draw_config = draw_config

        self.is_intersection: bool = False
        self.draging_node = None

        self.graph: Graph = graph

        self.bind("<B1-Motion>", self.drag)
        self.bind("<Motion>", self.change_cursor)
        self.bind("<ButtonRelease-1>", self.end_drag)
        self.bind("<Button-1>", self.start_drag)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)
        self.config(scrollregion=self.bbox(ctk.ALL))

    def toggle_intersection(self):
        self.is_intersection = not self.is_intersection
        if self.is_intersection:
            self.show_intersections()
        else:
            self.delete("intersection")

    def canvas_to_graph_coords(self, canvas_x, canvas_y):
        screen_x = self.canvasx(0)
        screen_y = self.canvasy(0)
        return canvas_x + screen_x, canvas_y + screen_y

    def set_edges(self, edges: list[Edge]):
        self.graph.edges = edges

    def set_nodes(self, nodes: list[Node]):
        self.graph.nodes = nodes

    def change_cursor(self, event):
        # change cursor when mouse if over node
        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for node in self.graph.nodes:
            if node.is_under_cursor(Vector(x, y)):
                return self.configure(cursor='hand1')

        self.configure(cursor='fleur')

    def drag(self, event):
        if self.draging_node:
            x, y = self.canvas_to_graph_coords(event.x, event.y)
            self.draging_node.position.x = x
            self.draging_node.position.y = y
            self.delete("all")
            self.draw_edges(self.graph.edges)
            self.draw_nodes(self.graph.nodes)
            return
        self.scan_dragto(event.x, event.y, gain=1)

    def start_drag(self, event):
        self.focus_set()

        x, y = self.canvas_to_graph_coords(event.x, event.y)
        for node in self.graph.nodes:
            if node.is_under_cursor(Vector(x, y)):
                node.is_selected = True
                self.graph.generator.select_nodes(node)
                self.draging_node = node
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.graph.generator.set_dragged_edges(self.graph.edges, node)
        if not self.draging_node:
            self.scan_mark(event.x, event.y)

    def end_drag(self, event):

        if self.draging_node:
            self.draging_node.is_dragged = False
            self.draging_node.radius = self.draw_config.node_radius

            self.graph.generator.set_dragged_edges(self.graph.edges, self.draging_node, False)
            self.draging_node = None
            self.draw_graph()
            return

        self.scan_dragto(event.x, event.y, gain=1)

    def reset_graph(self):
        self.graph.nodes.clear()
        self.graph.edges.clear()
        self.graph.path.clear()
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

        print(self.graph.edges)
        self.draw_nodes_and_edges()

    def search_path(self) -> tuple[float | None, list[int] | dict[int, list[int]]] | None:
        if algorithm_state.get_search_algorithm().min_selected_nodes == len(self.graph.generator.selected_nodes):
            distance, path = self.graph.generator.search_best_path(
                self.graph, self.graph.nodes, self.graph.generator.selected_nodes, algorithm_state.get_search_algorithm().algorithm_name)

            self.draw_path(path)
            if distance is None:
                return
            text = f"Distance: {distance}px"
            # check if distance is ininity
            if distance == math.inf:
                text = "No path found"

            self.create_text(20, 20, text=text, fill="white", anchor="w", tags="path")
            return distance, path

    def draw_intersections(self, intersections: list[tuple[float, float]]):
        self.create_text(20, 40, text=f"Intersections: {len(intersections)}",
                         fill="white", anchor="w", tags="intersection")
        for intersection in intersections:
            x, y = intersection
            self.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow", tags="intersection")

    def setup_intersections(self):
        self.graph.intersections = self.graph.generator.intersection.find_intersections(
            self.graph.edges, self.graph.nodes)

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
            self.draw_edge(edge)

    def draw_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.draw_node(node)

    def draw_node(self, node: Node):
        x0, y0, x1, y1 = self.graph.generator.get_node_oval_position(node)

        node.canvas_element = self.create_oval(
            x0, y0, x1, y1, fill=theme.get_node_color(node),
            outline="white", width=2, tags="node")
        self.create_text(node.position.x, node.position.y, text=str(node.index), fill="white", tags="node")

    def draw_edge(self, edge: Edge):
        self.create_line(
            edge.node1.position.x, edge.node1.position.y, edge.node2.position.x, edge.node2.position.y,
            fill=theme.get_edge_color(edge),
            width=theme.get_edge_width(edge),
            tags="edge")
