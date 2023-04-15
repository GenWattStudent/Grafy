import customtkinter as ctk
from src.graph.GraphModel import GraphModel
from src.ui.Menu.GraphMenu import GraphMenu
from src.ui.Menu.TreeMenu import TreeMenu
from src.ui.Menu.Menu import Menu
from src.Theme import Theme
from src.utils.Event import Event

class TabMenu(ctk.CTkFrame):
    def __init__(self, parent, graph: GraphModel, width, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = parent
        self.graph = graph
        self.width = width
        self.border_width = 2
        self.graph_menu_tab = GraphMenu(self, self.graph)
        self.tree_menu_tab = TreeMenu(self, self.graph)
        self.values = ["Graph", "Tree"]
        self.current_tab = self.values[0]
        self.current_tab_component: Menu  = self.get_component(self.current_tab)
        self.tab_view = ctk.CTkSegmentedButton(self, values=self.values, command=self.handle_tab_change)
        self.tab_view.set(self.current_tab)
        self.tab_view.pack(anchor="nw", fill="x", side="top")

        self.border = ctk.CTkLabel(self, text="", width=self.border_width, height=self.winfo_height(), fg_color=Theme.get("text_color"))
        self.tab_change_event = Event()

        self.bind("<Configure>", self.on_resize)
        self.handle_tab_change(self.current_tab)
        self.configure(width=width)

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
        self.current_tab = value
        if self.current_tab_component:
            self.current_tab_component.pack_forget()
        
        self.current_tab_component = self.get_component(value)
        self.current_tab_component.pack(anchor="nw", fill="both", side="left", expand=True)
        self.tab_change_event(value)

    def on_resize(self, event):
        self.border.configure(height=event.height)
        self.border.place(x=event.width - self.border_width, y=0)
        self.border.lift()

    def create_widgets(self):
        pass
