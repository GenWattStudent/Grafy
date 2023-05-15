import ttkbootstrap as ttk
from src.graph.GraphModel import GraphModel
from src.utils.Vector import Vector
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.elements.Intersection import Intersection
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.state.AlgorithmState import algorithm_state
from src.state.GraphState import graph_state
from src.graph.helpers.CanvasHelper import CanvasHelper
from src.Theme import theme
from ttkbootstrap.toast import ToastNotification
from src.ui.OptionMenu import OptionMenu, OptionMenuValue
from ttkbootstrap.dialogs import QueryDialog
import math as math
import threading
import uuid


class GraphCanvas(ttk.Canvas):
    def __init__(self, master, graph: GraphModel = GraphModel(), draw_config: DrawGraphConfig = DrawGraphConfig(), **kwargs):
        super().__init__(master, **kwargs)
        self.draw_config = draw_config
        self.is_intersection: bool = False
        self.draging_node: Node | None = None
        self.tab_id = uuid.uuid4()
        self.id = uuid.uuid4()
        self.active = False
        self._min_zoom = 1
        self._max_zoom = 10
        self.zoom_factor = 1

        self.graph: GraphModel = graph
        self.canvas_helper = CanvasHelper(self)

        self.configure(bg=theme.get("bg"))
        self.configure(scrollregion=self.bbox(ttk.ALL))
        self.bind("<Button-3>", self.right_click)
        self.bind("<MouseWheel>", self.zoom)

    def edit_value(self, node: Node):
        query = QueryDialog("Enter new value",initialvalue=str(node.value), title="Edit Node value")
        query.show()
        if query.result is not None:
            node.value = query.result
            node.update_width_depends_on_value()
        
        self.draw_graph()

    def right_click(self, event):
        el = self.canvas_helper.find_elemment_under_cursor(event, self.graph.get_graph_elements())
        if el is None or not isinstance(el, Node):
            return
        
        schema = [OptionMenuValue("Edit value", lambda: self.edit_value(el))]
        self.option_menu = OptionMenu(self, schema)
        self.option_menu.show(event)   
    
    def zoom(self, event):
        if event.delta > 0:
            if self.zoom_factor < self._max_zoom:
                self.scale("all", event.x, event.y, 1.1, 1.1)
                self.zoom_factor *= 1.1
        elif event.delta < 0:
            if self.zoom_factor > self._min_zoom:
                self.scale("all", event.x, event.y, 0.9, 0.9)
                self.zoom_factor *= 0.9
    
    def set_active(self, active: bool):
        self.active = active

        if active:
            self.configure(highlightthickness=3, highlightbackground=theme.get("primary"))
        else:
            self.configure(highlightthickness=0)

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
                return self.configure(cursor='hand2')

        self.configure(cursor='fleur')

    def reset_graph(self):
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
            self.graph.path = path
            graph_state.set(self.graph)
            return distance, path
        else:
            toast = ToastNotification(title="Warning", message=f"Select at least {algorithm_state.get_search_algorithm().min_selected_nodes} nodes", duration=4000)
            toast.show_toast()

    def draw_intersections(self, intersections: list[Intersection]):
        for intersection in intersections:
            intersection.draw(self)

    def setup_intersections(self):
        self.graph.intersections = self.graph.generator.intersection.find_intersections(self.graph.edges)

    def draw_graph(self):
        if self:
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

    def draw_edge_preview(self, event, node: Node):
        self.delete("edge_preview")
        x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
        return self.create_line(node.position.x, node.position.y, x, y, fill=theme.get("light"), width=2, tags="edge_preview")