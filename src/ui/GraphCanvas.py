import customtkinter as ctk
import src.constance as const
from src.Theme import theme
from src.graph.Graph import Graph
from src.utils.Vector import Vector
from src.graph.Node import Node
from src.graph.Edge import Edge
from src.graph.GraphHelper import GraphHelper
from src.graph.DrawHelper import DrawHelper
import math as math
import threading


class GraphCanvas(ctk.CTkCanvas):
    def __init__(self, master, graph: Graph, **kwargs):
        super().__init__(master, **kwargs)
        self.draw_helper = DrawHelper()
        self.is_paceked: bool = False
        self.is_intersection: bool = False
        self.draging_node = None

        self.graph: Graph = graph
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.path: list[int] = []
        self.intersection_points: list[tuple[float, float]] = []
        self.current_x: float = 0
        self.current_y: float = 0

        self.node_radius: int = 15
        self.width = const.SCREE_WIDTH
        self.height = const.SCREEN_HEIGHT

        self.bind('<Configure>', self.resize)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Motion>", self.change_cursor)
        self.bind("<ButtonRelease-1>", self.end_drag)
        self.bind("<Button-1>", self.start_drag)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def toggle_intersection(self):
        self.is_intersection = not self.is_intersection
        self.setup_intersections()
        self.draw_nodes_and_edges()

    def set_edges(self, edges: list[Edge]):
        self.edges = edges

    def set_nodes(self, nodes: list[Node]):
        self.nodes = nodes

    def set_is_intersection(self, is_intersection: bool):
        self.is_intersection = is_intersection
        if self.is_intersection:
            self.setup_intersections()

    def change_cursor(self, event):
        # change cursor when mouse if over node
        for node in self.nodes:
            if node.is_under_cursor(Vector(event.x, event.y)):
                self.configure(cursor='fleur')
                return
        self.configure(cursor='arrow')

    def resize(self, event):
        self.width = event.width
        self.height = event.height
        self.draw_graph()

    def drag(self, event):
        if self.draging_node:
            # move node and edges only if mouse is inside canvas
            if not GraphHelper.is_circle_out_of_bounds(self, event.x, event.y, self.draging_node.radius):
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
                self.draging_node.radius = 20
                self.draw_helper.set_dragged_edges(self.edges, node)
                break

    def end_drag(self, _):
        if self.draging_node:
            self.draging_node.is_dragged = False
            self.draging_node.radius = self.node_radius

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

    def draw_path(self, path: list[int]):
        self.delete("all")
        self.draw_helper.reset_edges_path(self.edges)
        # set is_path to true for all edges in path
        for i in range(len(path) - 1):
            for edge in self.edges:
                if edge.node1 == self.nodes[path[i]] and edge.node2 == self.nodes[path[i + 1]] or \
                        edge.node2 == self.nodes[path[i]] and edge.node1 == self.nodes[path[i + 1]]:
                    edge.is_path = True
                    break

        self.draw_nodes_and_edges()

    def search_path(self) -> tuple[float, list[int]] | None:
        first_selected_node = self.draw_helper.first_selected_node
        second_selected_node = self.draw_helper.second_selected_node

        if first_selected_node and second_selected_node:
            distance, path = self.draw_helper.search_best_path(
                self.graph, self.nodes, first_selected_node, second_selected_node)

            self.draw_path(path)
            text = f"Distance: {distance}px"
            # check if distance is ininity
            if distance == math.inf:
                text = "No path found"

            self.create_text(20, 20, text=text, fill="white", anchor="w")
            return distance, path

    def draw_intersections(self, intersections: list[tuple[float, float]]):
        self.create_text(20, 40, text=f"Intersections: {len(intersections)}", fill="white", anchor="w")
        for intersection in intersections:
            x, y = intersection
            self.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow")

    def setup_intersections(self):
        self.intersection_points = self.draw_helper.intersection.find_intersections(self.edges, self.nodes)

    def draw_graph(self):
        self.pack_canvas()
        self.reset_graph()

        self.nodes, self.edges = self.draw_helper.setup_graph(
            self.graph, self.node_radius, self.edges, self.winfo_width(), self.winfo_height())
        self.setup_intersections()
        self.draw_nodes_and_edges()

    def show_intersections(self):
        self.is_intersection = not self.is_intersection
        self.setup_intersections()
        self.draw_intersections(self.intersection_points)

    def draw_nodes_and_edges(self):
        self.delete("all")
        self.draw_edges(self.edges)
        if self.is_intersection:
            thread = threading.Thread(target=self.draw_intersections, args=(self.intersection_points,))
            thread.daemon = True
            thread.start()

        self.draw_nodes(self.nodes)

    def draw_edges(self, edges: list[Edge]):
        for edge in edges:
            self.draw_edge(edge)

    def draw_nodes(self, nodes: list[Node]):
        for node in nodes:
            self.draw_node(node)

    def draw_node(self, node: Node):
        x0, y0, x1, y1 = self.draw_helper.get_node_oval_position(node)

        self.create_oval(x0, y0, x1, y1, fill=theme.get_node_color(node), outline="white", width=2)
        self.create_text(node.position.x, node.position.y, text=str(node.index), fill="white")

    def draw_edge(self, edge: Edge):
        self.create_line(edge.node1.position.x, edge.node1.position.y, edge.node2.position.x,
                         edge.node2.position.y, fill=theme.get_edge_color(edge), width=theme.get_edge_width(edge))
