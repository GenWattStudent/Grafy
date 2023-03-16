import customtkinter as ctk
from src.utils.Event import Event
from src.inputs.Input import Input
from src.utils.validate.rules import Is_number, Min, Max, Is_float
from src.ui.Typography import Typography
from src.GraphHelper import GraphHelper
import src.State as State


number_of_nodes_rules = {
    "is_number": Is_number(),
    "min": Min(0),
    "max": Max(20),
}

probability_rules = {
    "is_number": Is_float(),
    "min": Min(0),
    "max": Max(1),
}


class Menu(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.number_of_nodes_change_event = Event()
        self.probability_change_event = Event()
        self.create_widgets()

    def on_number_of_nodes_change(self, cb):
        self.number_of_nodes_change_event += cb

    def off_number_of_nodes_change(self, cb):
        self.number_of_nodes_change_event -= cb

    def on_probability_change(self, cb):
        self.probability_change_event += cb

    def off_probability_change(self, cb):
        self.probability_change_event -= cb

    def create_matrix_wideget(self, matrix_string: str):
        self.matrix_tile_label = Typography(self, text="Matrix:", type="h2")
        self.matrix_label = Typography(self, text=matrix_string, type="h2", variant="success")

        self.matrix_tile_label.pack(anchor="w", padx=10, pady=5)
        self.matrix_label.pack()

    def create_widgets(self):
        self.label = Typography(self, text="Tools", type="h1")
        self.label.pack(side="top", pady=10, anchor="w", padx=10)

        self.number_of_nodes_entry = Input(self, "Number of nodes", 5, rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(self.number_of_nodes_change_event)
        self.number_of_nodes_entry.pack(anchor="w", padx=10, fill="x")

        self.probability_entry = Input(self, "Probability", 0.5, rules=probability_rules)
        self.probability_entry.on_change(self.probability_change_event)
        self.probability_entry.pack(anchor="w", padx=10, fill="x")

        if State.state['graph'] is not None:
            self.create_matrix_wideget(GraphHelper.get_matrix_string(State.state['graph']))
