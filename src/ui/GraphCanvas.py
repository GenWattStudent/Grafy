import customtkinter as ctk
import src.constance as const
from src.graph.GraphMatrix import GraphMatrix
from src.Theme import theme
from src.graph.Graph import Graph
from src.utils.Vector import Vector
from src.graph.Node import Node
from src.graph.Edge import Edge
from src.graph.GraphHelper import GraphHelper


class GraphCanvas(ctk.CTkCanvas):
    def __init__(self, master, graph: Graph, **kwargs):
        super().__init__(master, **kwargs)
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
            self.draging_node.position.x = event.x
            self.draging_node.position.y = event.y
            self.draw_nodes_and_edges(self.nodes, self.edges)

    def set_dragged_edges(self, node: Node, value: bool = True):
        for edge in self.edges:
            if edge.node1 == node or edge.node2 == node:
                edge.is_dragged = value

    def start_drag(self, event):
        self.focus_set()
        for node in self.nodes:
            if node.is_under_cursor(Vector(event.x, event.y)):
                node.is_dragged = True
                self.draging_node = node
                self.draging_node.radius = 20
                self.set_dragged_edges(node)
                break

    def end_drag(self, _):
        if self.draging_node:
            self.draging_node.is_dragged = False
            self.draging_node.radius = self.node_radius
            self.set_dragged_edges(self.draging_node, False)
            self.draging_node = None
            self.draw_nodes_and_edges(self.nodes, self.edges)

    def generate_random_node(self, node_id: int, radius: int) -> Node:
        max_x: float = self.winfo_width() - radius
        max_y: float = self.winfo_height() - radius
        vector: Vector = Vector().random(radius, max_x, radius, max_y)

        return Node(vector, node_id, radius)

    def generate_nodes(self) -> list[Node]:
        for i in range(self.graph.number_of_nodes):
            node: Node = self.generate_random_node(i + 1, self.node_radius)
            j = 0
            while j < 100 and GraphHelper.check_circle_overlap(
                    node.position.x, node.position.y, node.radius, self.nodes):
                node: Node = self.generate_random_node(i + 1, self.node_radius)
                j += 1

            self.nodes.append(node)
        return self.nodes

    def generate_edges(self, nodes: list[Node], graph: GraphMatrix, number_of_nodes: int) -> list[Edge]:
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

    def pack_canvas(self):
        if not self.is_paceked:
            self.pack(anchor="w", fill="both", expand=True, side="right")
            self.is_paceked = True

    def draw_graph(self):
        self.pack_canvas()
        self.reset_graph()
        nodes: list[Node] = self.generate_nodes()
        edges: list[Edge] = self.generate_edges(nodes, self.graph.graph, self.graph.number_of_nodes)

        self.draw_nodes_and_edges(nodes, edges)

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
        x0 = node.position.x - node.radius
        y0 = node.position.y - node.radius
        x1 = node.position.x + node.radius
        y1 = node.position.y + node.radius

        self.create_oval(x0, y0, x1, y1, fill=theme.get_node_color(node), outline="white", width=2)
        self.create_text(node.position.x, node.position.y, text=str(node.index), fill="white")

    def draw_edge(self, edge: Edge):
        self.create_line(edge.node1.position.x, edge.node1.position.y, edge.node2.position.x,
                         edge.node2.position.y, fill=theme.get_edge_color(edge))
