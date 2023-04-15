import customtkinter as ctk
from src.Theme import Theme
from src.ui.Menu.Menu import Menu
from src.graph.GraphModel import GraphModel
from src.inputs.Input import Input
from src.utils.validate.rules import Is_number, Min, Max, Is_positive
from src.ui.Typography import Typography, TextType
from src.state.GraphConfigState import graph_config_state
import src.constance as const

number_of_nodes_rules = {
    "is_positive": Is_positive(),
    "is_number": Is_number(),
    "min": Min(1),
    "max": Max(const.MAX_NODE_COUNT),
}


class TreeMenu(Menu):
    def __init__(self, parent, graph: GraphModel, border_width = 2, **kwargs):
        super().__init__(parent, graph, **kwargs)
        self.border_width = border_width
        self.create_widgets()

        self.border = ctk.CTkLabel(self, text="", width=self.border_width, height=self.winfo_height(), fg_color=Theme.get("text_color"))

        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        self.border.configure(height=event.height)
        self.border.place(x=event.width - self.border_width, y=0)

    def create_widgets(self):
        self.number_of_nodes_entry = Input(
            self, "Number of nodes", str(const.DEFAULT_NUMBER_OF_NODES), rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(lambda e: graph_config_state.set_number_of_nodes(int(e)))

        # self.button = ctk.CTkButton(self, text="Show Graph Details", command=self.show_matrix)
        # self.button.pack(padx=10, pady=10, fill="x")

        self.generate_graph_button = ctk.CTkButton(
            self, text="Generate tree", command=lambda e=graph_config_state.get(): self.generate_graph_event(e))
        self.generate_graph_button.pack(padx=10, pady=10, fill="x")
