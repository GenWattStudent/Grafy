import customtkinter as ctk
from src.Theme import theme
from src.graph.Graph import Graph
from src.utils.Vector import Vector
from src.graph.Node import Node
from src.graph.Edge import Edge
from src.graph.GraphHelper import GraphHelper
from src.graph.DrawHelper import DrawHelper
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.state.AlgorithmState import algorithm_state
import math as math
from src.layout.Kwaii import TarjanSCC
import threading


class GraphCanvas(ctk.CTkCanvas):
    def __init__(self, master, graph: Graph, **kwargs):
        super().__init__(master, **kwargs)
        self.draw_helper = DrawHelper()
        self.draw_config = DrawGraphConfig()

        self.is_paceked: bool = False
        self.is_intersection: bool = False
        self.draging_node = None

        self.graph: Graph = graph
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.path: list[int] = []
        self.intersection_points: list[tuple[float, float]] = []

        self.layout = TarjanSCC(self, self.winfo_width(), self.winfo_height())
        self.layout.run()
        self.bind('<Configure>', self.resize)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Motion>", self.change_cursor)
        self.bind("<ButtonRelease-1>", self.end_drag)
        self.bind("<Button-1>", self.start_drag)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def toggle_intersection(self):
        self.is_intersection = not self.is_intersection
        if self.is_intersection:
            self.show_intersections()
        else:
            self.delete("intersection")

    def set_edges(self, edges: list[Edge]):
        self.edges = edges

    def set_nodes(self, nodes: list[Node]):
        self.nodes = nodes

    def change_cursor(self, event):
        # change cursor when mouse if over node
        for node in self.nodes:
            if node.is_under_cursor(Vector(event.x, event.y)):
                return self.configure(cursor='fleur')

        self.configure(cursor='arrow')

    def resize(self, event):
        self.draw_config.width = event.width
        self.draw_config.height = event.height
        self.draw_graph()

    def drag(self, event):
        if self.draging_node:
            # move node and edges only if mouse is inside canvas
            if not GraphHelper.is_circle_out_of_bounds(
                    self, event.x, event.y - self.draw_config.y_margin, self.draging_node.radius):
                self.draging_node.position.x = event.x
                self.draging_node.position.y = event.y
                self.delete("all")
                self.draw_edges(self.edges)
                self.draw_nodes(self.nodes)

    def start_drag(self, event):
        self.focus_set()
        for node in self.nodes:
            if node.is_under_cursor(Vector(event.x, event.y)):
                node.is_selected = True
                self.draw_helper.select_nodes(node)
                self.draging_node = node
                self.draging_node.radius = self.draw_config.dragged_node_radius
                self.draw_helper.set_dragged_edges(self.edges, node)
                break

    def end_drag(self, _):
        if self.draging_node:
            self.draging_node.is_dragged = False
            self.draging_node.radius = self.draw_config.node_radius

            self.draw_helper.set_dragged_edges(self.edges, self.draging_node, False)
            self.draging_node = None
            self.setup_intersections()
            self.draw_nodes_and_edges()

    def reset_graph(self):
        self.nodes.clear()
        self.edges.clear()
        self.path.clear()
        self.intersection_points.clear()
        self.draw_helper.reset_edges_path(self.edges)
        self.delete("all")

    def pack_canvas(self):
        if not self.is_paceked:
            self.pack(anchor="w", fill="both", expand=True, side="right")
            self.is_paceked = True

    def draw_path(self, path: list[int] | dict[int, list[int]]):
        self.delete("all")
        self.draw_helper.reset_edges_path(self.edges)
        # print(path)
        # set is_path to true for all edges in path
        if isinstance(path, list):
            for i in range(len(path) - 1):
                for edge in self.edges:
                    if edge.node1 == self.nodes[path[i]] and edge.node2 == self.nodes[path[i + 1]] or \
                            edge.node2 == self.nodes[path[i]] and edge.node1 == self.nodes[path[i + 1]]:
                        edge.is_path = True

        elif isinstance(path, dict):
            # draw path from dictionary
            print(path)
            for key, value in path.items():
                for edge in self.edges:
                    if edge.node1.get_index() == key and edge.node2.get_index() in value or \
                            edge.node2.get_index() == key and edge.node1.get_index() in value:
                        edge.is_path = True

        self.draw_nodes_and_edges()

    def search_path(self) -> tuple[float | None, list[int] | dict[int, list[int]]] | None:
        if algorithm_state.get_search_algorithm().min_selected_nodes == len(self.draw_helper.selected_nodes):
            distance, path = self.draw_helper.search_best_path(
                self.graph, self.nodes, self.draw_helper.selected_nodes, algorithm_state.get_search_algorithm().algorithm_name)

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
        self.intersection_points = self.draw_helper.intersection.find_intersections(self.edges, self.nodes)

    def draw_graph(self):
        self.pack_canvas()
        self.reset_graph()

        self.nodes, self.edges = self.draw_helper.setup_graph(
            self.graph, self.draw_config.node_radius, self.edges, self.winfo_width(), self.winfo_height())

        self.draw_nodes_and_edges()

    def show_intersections(self):
        if self.is_intersection:
            self.setup_intersections()
            thread = threading.Thread(target=self.draw_intersections, args=(self.intersection_points,))
            thread.daemon = True
            thread.start()

    def draw_nodes_and_edges(self):
        self.delete("all")
        self.draw_edges(self.edges)
        if self.is_intersection:
            self.show_intersections()
            self.draw_intersections(self.intersection_points)

        self.draw_nodes(self.nodes)

    def draw_edges(self, edges: list[Edge]):
        self.delete("edge")
        for edge in edges:
            self.draw_edge(edge)

    def draw_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.draw_node(node)

    def draw_node(self, node: Node):
        x0, y0, x1, y1 = self.draw_helper.get_node_oval_position(node)

        self.create_oval(x0, y0, x1, y1, fill=theme.get_node_color(node), outline="white", width=2, tags="node")
        self.create_text(node.position.x, node.position.y, text=str(node.index), fill="white", tags="node")

    def draw_edge(self, edge: Edge):
        self.create_line(
            edge.node1.position.x, edge.node1.position.y, edge.node2.position.x, edge.node2.position.y,
            fill=theme.get_edge_color(edge),
            width=theme.get_edge_width(edge),
            tags="edge")
