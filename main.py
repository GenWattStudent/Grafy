import customtkinter as ctk
from src.GraphFile import GraphFile
from src.graph.GraphModel import GraphModel
from src.ui.Menu.TabMenu import TabMenu
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
        self.graph_model = GraphModel()
        self.frame = ctk.CTkFrame(self)
        self.draw_graph_config: DrawGraphConfig = DrawGraphConfig()
        self.graph_view = GraphCanvas(self, draw_config = self.draw_graph_config)
        self.toolbar = ToolBar(self.frame, self, self.graph_model)
        self.tab_menu = TabMenu(parent=self, width=const.SCREEN_WIDTH / 5, graph=self.graph_model)
        self.controller = GraphController(self.graph_view, self.toolbar, GraphFile(filename="graph.txt"), self.tab_menu.current_tab)

        self.setup_window()

    def on_search_path(self):
        self.controller.view.search_path()

    def setup_window(self):
        self.title("Grafy lalala")
        self.geometry('%dx%d+%d+%d' % (const.SCREEN_WIDTH, const.SCREEN_HEIGHT, 0, 0))
        # bind events
        self.tab_menu.on_search_path(self.on_search_path)
        self.tab_menu.on_generate_graph(self.controller.create)
        self.tab_menu.on_tab_change(self.controller.change_mode)
        # add observers
        graph_config_state.subscribe(self.controller.update)
        graph_state.subscribe(self.controller.file_manager.save)
        # pack widgets
        self.tab_menu.pack(anchor="nw", fill="y", side="left")
        self.tab_menu.pack_propagate(False)

        self.graph_view.pack(anchor="s", fill="both", expand=True, side="bottom")
        self.toolbar.pack(anchor="n", side="top", fill="x")
        self.frame.pack(anchor="nw", fill="both", expand=True, side="right")
        self.update()
        # create array of nodes and draw graph
        self.controller.create(graph_config_state.get())
        self.mainloop()


App()
