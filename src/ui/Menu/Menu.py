import ttkbootstrap as ttk
from src.utils.Event import Event
from abc import abstractmethod
from src.graph.GraphController import GraphController

class Menu(ttk.Frame):
    def __init__(self, parent, controller: GraphController, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = parent
        self.controller = controller
        self.graph_model = controller.current_graph.get()

        self.search_path_event = Event()
        self.generate_graph_event = Event()
        self.isomorphic_var = ttk.StringVar(value="Isomorphic: off")
    
    def get_isomorphic_string(self, graphs: list[str]) -> str:
        string = ''
        for  graph in graphs:
            string += f"{graph}, "
        
        return string[:-2]

    def set_isomorphic_var(self, graphs: list[str], is_isomorphic: bool | None):
        if  is_isomorphic is None:
            self.isomorphic_var.set("Isomorphic: off")
            return
        if is_isomorphic:
            string = self.get_isomorphic_string(graphs)
            string += " are isomorphic"
            self.isomorphic_var.set(string)
        else:
            string = self.get_isomorphic_string(graphs)
            string += " are not isomorphic"
            self.isomorphic_var.set(string)

    def on_search_path(self, cb):
        self.search_path_event += cb
    
    def off_search_path(self, cb):
        self.search_path_event -= cb

    def on_generate_graph(self, cb):
        self.generate_graph_event += cb
    
    def off_generate_graph(self, cb):
        self.generate_graph_event -= cb

    def init(self):
        pass

    @abstractmethod
    def create_widgets(self):
        pass

    @abstractmethod
    def destroy(self):
        super().destroy()

