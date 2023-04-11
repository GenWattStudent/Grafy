import customtkinter as ctk
from src.graph.Graph import Graph
from src.GraphFile import GraphFile
from src.ui.Menu import Menu
from src.ui.GraphCanvas import GraphCanvas
from src.state.GraphConfigState import graph_config_state
from src.state.GraphState import graph_state
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.graph.GraphController import GraphController
from src.ui.Toolbar import ToolBar
import src.constance as const


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.graph: Graph = Graph(file_manager=GraphFile(filename="graph.txt"))
        self.frame = ctk.CTkFrame(self)
        self.menu = Menu(parent=self, width=const.SCREEN_WIDTH / 5, graph=self.graph)
        self.toolbar = ToolBar(self.frame, self.graph)
        self.draw_graph_config: DrawGraphConfig = DrawGraphConfig()
        self.graph_view = GraphCanvas(self, self.graph, self.draw_graph_config)
        self.controller = GraphController(self.graph, self.graph_view, self.toolbar, GraphFile(filename="graph.txt"))

        self.setup_window()

    def on_search_path(self):
        self.controller.view.search_path()
        if self.controller.model.file_manager:
            self.controller.model.file_manager.save(self.controller.model)

    def setup_window(self):
        self.title("Grafy lalala")
        self.geometry('%dx%d+%d+%d' % (const.SCREEN_WIDTH, const.SCREEN_HEIGHT, 0, 0))
        # bind events
        self.menu.on_search_path(self.on_search_path)
        self.menu.on_generate_graph(self.controller.create)
        # add observers
        graph_config_state.subscribe(self.controller.update)
        graph_state.subscribe(self.graph.file_manager.save)
        # pack widgets
        self.menu.pack(anchor="nw",  fill="y", side="left")
        self.menu.pack_propagate(False)

        self.graph_view.pack(anchor="s", fill="both", expand=True, side="bottom")
        self.toolbar.pack(anchor="n", side="top", fill="x")
        self.frame.pack(anchor="nw", fill="both", expand=True, side="right")
        self.update()
        # create array of nodes and draw graph
        self.controller.create(graph_config_state.get())
        self.mainloop()


App()
