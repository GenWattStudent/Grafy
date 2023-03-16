import customtkinter as ctk
from src.Graph import Graph
from src.ManageFiles import ManageFiles
from src.ui.Menu import Menu
from src.ui.GraphCanvas import GraphCanvas
import src.State as State


class App:
    def __init__(self):
        self.probability: float = 0.5
        self.number_of_nodes: int = 5
        self.graph: Graph = Graph()

        self.setup_window()

    def create_graph(self, number_of_nodes, probability):
        self.graph.set_number_of_nodes(number_of_nodes)
        self.graph.set_probability(probability)
        State.state['graph'] = self.graph.generate_graph()

        self.save_graph()

    def save_graph(self):
        self.manage_files = ManageFiles(filename="graph.txt")
        self.manage_files.save_graph_with_students_info(self.graph.get_graph())

    def on_number_of_node_change(self, value):
        if value.isdigit() and int(value) > 0 and int(value) < 100:
            self.number_of_nodes = int(value)
            self.create_graph(self.number_of_nodes, self.probability)
            self.canvas.draw_graph()

    def on_probability_change(self, value):
        # check if value is float and if it is between 0 and 1
        try:
            if float(value) >= 0 and float(value) <= 1:
                self.probability = float(value)
                self.create_graph(self.number_of_nodes, self.probability)
                self.canvas.draw_graph()
        except ValueError:
            pass

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Grafy lalala")
        self.root.geometry("800x800")
        # create array of nodes
        self.create_graph(5, 0.5)
        # create ui
        self.menu = Menu(self.root, width=200)
        self.canvas = GraphCanvas(self.root, self.graph)
        self.canvas.draw_graph()
        # bind events
        self.menu.on_number_of_nodes_change(self.on_number_of_node_change)
        self.menu.on_probability_change(self.on_probability_change)
        # pack widgets
        self.menu.pack(anchor="nw",  fill="y", side="left")
        self.menu.pack_propagate(0)
        self.canvas.pack(anchor="w", fill="both", expand=True, side="right")
        self.root.mainloop()


App()
