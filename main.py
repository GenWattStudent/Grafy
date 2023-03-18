import customtkinter as ctk
from src.graph.Graph import Graph
from src.ManageFiles import ManageFiles
from src.ui.Menu import Menu
from src.ui.GraphCanvas import GraphCanvas
from src.observers.graph.GraphSensor import graph_state
from src.observers.graph.GraphObserver import GraphObserver
from src.graph.GraphMatrix import GraphMatrix
import src.constance as const


class App:
    def __init__(self):
        self.probability: float = const.DEFAULT_PROBABILITY
        self.number_of_nodes: int = const.DEFAULT_NUMBER_OF_NODES
        self.graph: Graph = Graph()

        self.setup_window()

    def create_graph(self, number_of_nodes, probability):
        self.graph.set_number_of_nodes(number_of_nodes)
        self.graph.set_probability(probability)
        self.graph.generate_graph()
        graph_state.graph = self.graph.get_graph()

    def save_graph(self, matrix: GraphMatrix):
        self.manage_files = ManageFiles(filename="graph.txt")
        self.manage_files.save_graph_with_students_info(matrix)

    def on_number_of_node_change(self, value):
        self.number_of_nodes = int(value)
        self.create_graph(self.number_of_nodes, self.probability)
        self.canvas.draw_graph()

    def on_probability_change(self, value):
        self.probability = float(value)
        self.create_graph(self.number_of_nodes, self.probability)
        self.canvas.draw_graph()

    def on_search_path(self):
        self.canvas.search_path()

    def on_toogle_intersection(self):
        self.canvas.toggle_intersection()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Grafy lalala")
        self.root.geometry('%dx%d+%d+%d' % (const.SCREE_WIDTH, const.SCREEN_HEIGHT, 0, 0))
        # create ui
        self.menu = Menu(self.root, width=const.SCREE_WIDTH / 5)
        self.canvas = GraphCanvas(self.root, self.graph)
        # bind events
        self.menu.on_number_of_nodes_change(self.on_number_of_node_change)
        self.menu.on_probability_change(self.on_probability_change)
        self.menu.on_search_path(self.on_search_path)
        self.menu.on_toogle_intersection(self.on_toogle_intersection)
        # add observers
        self.graph_observer = GraphObserver(self.save_graph)
        graph_state.add_observer(self.graph_observer)
        # pack widgets
        self.menu.pack(anchor="nw",  fill="y", side="left")
        self.menu.pack_propagate(False)
        # create array of nodes and draw graph
        self.create_graph(self.number_of_nodes, self.probability)
        self.canvas.draw_graph()

        self.root.mainloop()


App()
