import customtkinter as ctk
from src.graph.Graph import Graph
from src.ManageFiles import ManageFiles
from src.ui.Menu import Menu
from src.graph.DrawGraph import DrawGraph
from src.state.GraphState import graph_state
from src.state.GraphConfigState import graph_config_state, GraphConfig
from src.graph.GraphMatrix import GraphMatrix
import src.constance as const
from typing import Any


class App:
    def __init__(self):
        self.graph: Graph = Graph()

        self.setup_window()

    def setup_graph(self, config: GraphConfig):
        self.graph.set_number_of_nodes(config.number_of_nodes)
        self.graph.set_probability(config.probability)
        self.graph.generate_graph()
        graph_state.set(self.graph.get_graph())

    def is_state_value_changed(self, current_value: Any, prev_value: Any, value_prop_name: str) -> bool:
        return getattr(prev_value, value_prop_name) != getattr(current_value, value_prop_name)

    def update_graph(self, config: GraphConfig, prev_config: GraphConfig):
        if not config.draw_on_input_change:
            return

        if self.is_state_value_changed(config, prev_config, "is_show_intersections"):
            return self.canvas.update_intersections()

        if self.is_state_value_changed(config, prev_config, "probability"):
            self.setup_graph(config)
            return self.canvas.update_probability()

        if self.is_state_value_changed(config, prev_config, "number_of_nodes"):
            self.setup_graph(config)
            return self.canvas.update_number_of_nodes()

    def create_graph(self, config: GraphConfig):
        self.setup_graph(config)
        self.canvas.draw_graph()

    def save_graph(self, matrix: GraphMatrix, _):
        ManageFiles(filename="graph.txt").save_graph_with_students_info(matrix)

    def on_search_path(self):
        self.canvas.search_path()

    def setup_window(self):
        self.root = ctk.CTk()
        self.root.title("Grafy lalala")
        self.root.geometry('%dx%d+%d+%d' % (const.SCREE_WIDTH, const.SCREEN_HEIGHT, 0, 0))
        # create ui
        self.menu = Menu(self.root, width=const.SCREE_WIDTH / 5)
        self.canvas = DrawGraph(self.root, self.graph)
        # bind events
        self.menu.on_search_path(self.on_search_path)
        self.menu.on_generate_graph(self.create_graph)
        # add observers
        graph_state.subscribe(self.save_graph)
        graph_config_state.subscribe(self.update_graph)
        # pack widgets
        self.menu.pack(anchor="nw",  fill="y", side="left")
        self.menu.pack_propagate(False)
        # create array of nodes and draw graph
        self.create_graph(graph_config_state.get())

        self.root.mainloop()


App()
