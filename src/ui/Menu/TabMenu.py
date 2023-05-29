from __future__ import annotations
import ttkbootstrap as ttk
from src.graph.GraphModel import GraphModel
from src.ui.Menu.GraphMenu import GraphMenu
from src.ui.Menu.TreeMenu import TreeMenu
from src.ui.Menu.Menu import Menu
from src.utils.Event import Event
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController

class TabMenu(ttk.Frame):
    def __init__(self, parent, controller: GraphController, width, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = parent
        self.controller = controller
        self.width = width
        self.border_width = 2
        self.current_tab = "Graph"
        self.tab_view = ttk.Notebook(self)

        self.graph_menu_tab = GraphMenu(self.tab_view, parent, controller)
        self.tree_menu_tab = TreeMenu(self.tab_view, parent, controller)
        self.current_tab_component: Menu  = self.get_component(self.current_tab)

        self.tab_view.pack(anchor="nw", fill="x", side="top", expand=True)
        self.tab_view.add(self.graph_menu_tab, text="Graph")
        self.tab_view.add(self.tree_menu_tab, text="Tree")
        self.tab_view.bind("<<NotebookTabChanged>>", self.handle_tab_change)
  
        self.border = ttk.Label(self, text="", width=self.border_width, style="PRIMARY.TButton")
        self.tab_change_event = Event()

        self.bind("<Configure>", self.on_resize)
        self.configure(width=width)

    def set_graph(self, graph: GraphModel):
        self.graph = graph
        self.graph_menu_tab.graph_model = graph
        self.tree_menu_tab.graph_model = graph

    def on_tab_change(self, cb):
        self.tab_change_event += cb
    
    def off_tab_change(self, cb):
        self.tab_change_event -= cb

    def on_search_path(self, cb):
        self.graph_menu_tab.search_path_event += cb
        self.tree_menu_tab.search_path_event += cb

    def off_search_path(self, cb):
        self.graph_menu_tab.search_path_event -= cb
        self.tree_menu_tab.search_path_event -= cb

    def on_generate_graph(self, cb):
        self.graph_menu_tab.generate_graph_event += cb
        self.tree_menu_tab.generate_graph_event += cb
    
    def off_generate_graph(self, cb):
        self.graph_menu_tab.generate_graph_event -= cb
        self.tree_menu_tab.generate_graph_event -= cb

    def get_component(self, value: str) -> "Menu":
        if value == "Graph":
            return self.graph_menu_tab
        else:
            return self.tree_menu_tab

    def handle_tab_change(self, value):
        self.current_tab = value.widget.tab(value.widget.select(), "text")
        self.tab_change_event(self.current_tab)

    def on_resize(self, event):
        self.border.place(relx=0.99, relheight=1, y=0)
        self.border.lift()

    def create_widgets(self):
        pass
