import customtkinter as ctk
from src.graph.Graph import Graph
from src.ManageFiles import ManageFiles
from src.ui.Menu import Menu
from src.ui.GraphCanvas import GraphCanvas
from src.state.GraphState import graph_state
from src.state.GraphConfigState import graph_config_state, GraphConfig
from src.graph.GraphMatrix import GraphMatrix
from src.graph.DrawGraphConfig import DrawGraphConfig
import src.constance as const


class App:
    def __init__(self):
        self.graph: Graph = Graph()
        self.draw_graph_config: DrawGraphConfig = DrawGraphConfig()

        self.setup_window()

    def update_graph(self, config: GraphConfig):
        matrix = self.graph.update(config, self.canvas)
        self.canvas.is_intersection = config.is_show_intersections
        self.canvas.draw_graph()
        print(matrix)
        graph_state.set(matrix)

    def create_graph(self, config: GraphConfig):
        self.graph.update(config, self.canvas)
        matrix = self.graph.create(self.canvas)
        self.canvas.is_intersection = config.is_show_intersections
        self.canvas.draw_graph()
        graph_state.set(matrix)

    def save_graph(self, matrix: GraphMatrix):
        ManageFiles(filename="graph.txt").save_graph_with_students_info(matrix)

    def on_search_path(self):
        self.canvas.search_path()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Grafy lalala")
        self.root.geometry('%dx%d+%d+%d' % (const.SCREEN_WIDTH, const.SCREEN_HEIGHT, 0, 0))
        # create ui
        self.menu = Menu(self.root, width=const.SCREEN_WIDTH / 5)
        self.canvas = GraphCanvas(self.root, self.graph, self.draw_graph_config)
        # bind events
        self.menu.on_search_path(self.on_search_path)
        self.menu.on_generate_graph(self.create_graph)
        # add observers
        graph_state.subscribe(self.save_graph)
        graph_config_state.subscribe(self.update_graph)
        # pack widgets
        self.menu.pack(anchor="nw",  fill="y", side="left")
        self.menu.pack_propagate(False)
        self.canvas.pack(anchor="w", fill="both", expand=True)
        self.root.update()
        # create array of nodes and draw graph
        self.create_graph(graph_config_state.get())

        self.root.mainloop()


App()
