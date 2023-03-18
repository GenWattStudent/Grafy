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


class GraphCanvas(ctk.CTkCanvas):
    def __init__(self, master, graph: Graph, **kwargs):
        super().__init__(master, **kwargs)
        self.draw_helper = DrawHelper()
        self.is_paceked: bool = False
        self.graph: Graph = graph
        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.node_radius: int = 15
        self.width = const.SCREE_WIDTH
        self.height = const.SCREEN_HEIGHT
        self.draging_node = None

        self.bind('<Configure>', self.resize)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<Motion>", self.change_cursor)
        self.bind("<ButtonRelease-1>", self.end_drag)
        self.bind("<Button-1>", self.start_drag)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

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
            self.is_dragging = True
            # move node and edges only if mouse is inside canvas
            if not GraphHelper.is_circle_out_of_bounds(self, event.x, event.y, self.draging_node.radius):
                self.draging_node.position.x = event.x
                self.draging_node.position.y = event.y
                self.draw_nodes_and_edges(self.nodes, self.edges)

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
            self.draw_nodes_and_edges(self.nodes, self.edges)

    def reset_graph(self):
        self.nodes.clear()
        self.edges.clear()
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

        self.draw_edges(self.edges)
        self.draw_nodes(self.nodes)

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

            self.create_text(80, 20, text=text, fill="white")
            return distance, path

    def draw_graph(self):
        self.pack_canvas()
        self.reset_graph()

        self.nodes: list[Node] = self.draw_helper.generate_nodes(
            self.graph, self.node_radius, self.winfo_width(), self.winfo_height())

        self.edges: list[Edge] = self.draw_helper.generate_edges(self.nodes, self.graph)
        self.draw_nodes_and_edges(self.nodes, self.edges)

    def draw_nodes_and_edges(self, nodes: list[Node], edges: list[Edge]):
        self.delete("all")
        self.draw_edges(edges)
        self.draw_nodes(nodes)

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
