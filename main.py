import customtkinter as ctk
from src.GenerateGraph import Graph
from src.ManageFiles import ManageFiles
from src.ui.Menu import Menu


class App:
    def __init__(self):
        self.probability = 0.5
        self.number_of_nodes = 5
        self.graph = Graph()
        self.setup_window()

    def create_graph(self, number_of_nodes, probability):
        self.graph.set_number_of_nodes(number_of_nodes)
        self.graph.set_probability(probability)
        self.graph.generate_graph()

        self.save_graph()

    def save_graph(self):
        self.manage_files = ManageFiles(filename="graph.txt")
        self.manage_files.save_graph_with_students_info(self.graph.get_graph())

    def on_number_of_node_change(self, value):
        if value.get().isdigit() and int(value.get()) > 0 and int(value.get()) < 100:
            self.number_of_nodes = int(value.get())
            self.create_graph(self.number_of_nodes, self.probability)

    def on_probability_change(self, value):
        # check if value is float and if it is between 0 and 1
        try:
            if float(value.get()) >= 0 and float(value.get()) <= 1:
                self.probability = float(value.get())
                self.create_graph(self.number_of_nodes, self.probability)
        except ValueError:
            pass

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Grafy lalala")
        self.root.geometry("800x800")
        self.menu = Menu(self.root)

        self.create_graph(5, 0.5)
        self.menu.on_number_of_nodes_change(self.on_number_of_node_change)
        self.menu.on_probability_change(self.on_probability_change)
        self.menu.pack(anchor="nw", expand=True, fill="y")
        self.root.mainloop()


App()
