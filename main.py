import ttkbootstrap as ttk 
from src.fillesystem.XMLFileGraph import XMLFileGraph
from src.graph.GraphModel import GraphModel
from src.ui.Menu.TabMenu import TabMenu
from src.ui.GraphCanvas import GraphCanvas
from src.state.GraphConfigState import graph_config_state
from src.state.GraphState import graph_state
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.graph.GraphController import GraphController
from src.ui.Toolbar import ToolBar
from src.Theme import theme
import src.constance as const


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        string = str(self.style.colors)
        string = string.replace("(", "").replace(")", "").replace("'", "").replace(" ", "").split(",")
        for i in range(len(string)):
           if i % 2 == 0:
                theme.set(string[i], string[i + 1])

        print(theme.theme)
        self.graph_model = GraphModel()
        self.frame = ttk.Frame(self)
        self.draw_graph_config: DrawGraphConfig = DrawGraphConfig()
        self.graph_view = GraphCanvas(self, draw_config = self.draw_graph_config)
        self.toolbar = ToolBar(self.frame, self, self.graph_model)
        self.controller = GraphController(self, self.graph_view, self.toolbar, XMLFileGraph())
        self.tab_menu = TabMenu(parent=self, width=const.SCREEN_WIDTH / 5, controller = self.controller)
        self.controller.tab_menu = self.tab_menu # type: ignore
        
        self.setup_window()

    def on_search_path(self):
        self.controller.view.search_path()
    
    def update_menu(self, e: GraphModel):
        self.tab_menu.set_graph(e)

    def setup_window(self):
        self.title("Grafy lalala")
        self.geometry('%dx%d+%d+%d' % (const.SCREEN_WIDTH, const.SCREEN_HEIGHT, 0, 0))
        # bind events
        self.tab_menu.on_search_path(self.on_search_path)
        self.tab_menu.on_generate_graph(self.controller.create)
        self.tab_menu.on_tab_change(self.controller.change_mode)
        # add observers
        graph_config_state.subscribe(self.controller.update)
        graph_state.subscribe(lambda e: self.controller.useless_graph_file.save(e, ""))
        graph_state.subscribe(self.update_menu)
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
