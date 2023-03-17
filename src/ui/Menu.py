import customtkinter as ctk
from src.utils.Event import Event
from src.inputs.Input import Input
from src.utils.validate.rules import Is_number, Min, Max, Is_float, Is_positive
from src.ui.Typography import Typography
from src.graph.GraphHelper import GraphHelper
from src.observers.graph.GraphSensor import graph_state
from src.observers.graph.GraphObserver import GraphObserver
from src.graph.GraphMatrix import GraphMatrix
from src.ui.Matrix import Matrix
import src.constance as const


number_of_nodes_rules = {
    "is_positive": Is_positive(),
    "is_number": Is_number(),
    "min": Min(0),
    "max": Max(const.MAX_NODE_COUNT),
}

probability_rules = {
    "is_positive": Is_positive(),
    "is_float": Is_float(),
    "min": Min(0),
    "max": Max(1),
}


class Menu(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.number_of_nodes_change_event = Event()
        self.probability_change_event = Event()
        self.create_widgets()

        self.label = ctk.CTkLabel(self, text="", width=2, height=const.SCREEN_HEIGHT, fg_color="white")
        self.label.place(x=198, y=0)

    def on_number_of_nodes_change(self, cb):
        self.number_of_nodes_change_event += cb

    def off_number_of_nodes_change(self, cb):
        self.number_of_nodes_change_event -= cb

    def on_probability_change(self, cb):
        self.probability_change_event += cb

    def off_probability_change(self, cb):
        self.probability_change_event -= cb

    def create_matrix_wideget(self, matrix: GraphMatrix):
        self.matrix_widget = Matrix(self, matrix)
        self.matrix_widget.draw()
        self.matrix_widget.pack(pady=10, padx=10)

    def update_matrix_wideget(self, matrix: GraphMatrix):
        if not hasattr(self, "matrix_widget"):
            self.create_matrix_wideget(matrix)
        self.matrix_widget.update_wideget(matrix)

    def create_widgets(self):
        self.graph_observer = GraphObserver(self.update_matrix_wideget)
        graph_state.add_observer(self.graph_observer)

        self.label = Typography(self, text="Tools", type="h1")
        self.label.pack(side="top", pady=10, anchor="w", padx=10)

        self.number_of_nodes_entry = Input(
            self, "Number of nodes", const.DEFAULT_NUMBER_OF_NODES, rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(self.number_of_nodes_change_event)

        self.probability_entry = Input(self, "Probability", const.DEFAULT_PROBABILITY, rules=probability_rules)
        self.probability_entry.on_change(self.probability_change_event)
        self.probability_entry.pack(anchor="w", padx=10, fill="x")
