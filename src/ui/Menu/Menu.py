import customtkinter as ctk
from src.utils.Event import Event
from abc import abstractmethod
from src.graph.GraphModel import GraphModel


class Menu(ctk.CTkFrame):
    def __init__(self, parent, graph_model: GraphModel, **kwargs):
        super().__init__(parent, **kwargs)
        self.root = parent
        self.graph_model = graph_model

        self.search_path_event = Event()
        self.generate_graph_event = Event()

    def on_search_path(self, cb):
        self.search_path_event += cb
    
    def off_search_path(self, cb):
        self.search_path_event -= cb

    def on_generate_graph(self, cb):
        self.generate_graph_event += cb
    
    def off_generate_graph(self, cb):
        self.generate_graph_event -= cb

    @abstractmethod
    def create_widgets(self):
        pass

    @abstractmethod
    def destroy(self):
        super().destroy()

