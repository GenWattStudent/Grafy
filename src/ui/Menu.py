import customtkinter as ctk
from src.utils.Event import Event
from src.inputs.Input import Input
from src.utils.validate.rules import Is_number, Min, Max, Is_float, Is_positive
from src.ui.Typography import Typography, TextType
from src.observers.graph.GraphSensor import graph_state
from src.observers.graph.GraphObserver import GraphObserver
from src.graph.GraphMatrix import GraphMatrix
from src.ui.windows.MatrixWindow import MatrixWindow
import src.constance as const


number_of_nodes_rules = {
    "is_positive": Is_positive(),
    "is_number": Is_number(),
    "min": Min(1),
    "max": Max(const.MAX_NODE_COUNT),
}

probability_rules = {
    "is_float": Is_float(),
    "is_positive": Is_positive(),
    "min": Min(0),
    "max": Max(1),
}


class Menu(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        ctk.CTkFrame.__init__(self, parent, **kwargs)
        self.number_of_nodes_change_event = Event()
        self.probability_change_event = Event()
        self.search_path_event = Event()
        self.border_width = 2
        self.is_matrix_window_open = False
        self.create_widgets()

        self.label = ctk.CTkLabel(self, text="", width=self.border_width, height=const.SCREEN_HEIGHT, fg_color="white")

    def on_number_of_nodes_change(self, cb):
        self.number_of_nodes_change_event += cb

    def off_number_of_nodes_change(self, cb):
        self.number_of_nodes_change_event -= cb

    def on_probability_change(self, cb):
        self.probability_change_event += cb

    def off_probability_change(self, cb):
        self.probability_change_event -= cb

    def on_search_path(self, cb):
        self.search_path_event += cb

    def off_search_path(self, cb):
        self.search_path_event -= cb

    def update_matrix_window(self, matrix: GraphMatrix):
        if hasattr(self, "matrix_window") and self.matrix_window is not None:
            return self.matrix_window.update_matrix(matrix)

    def create_matrix(self, matrix: GraphMatrix | None):
        if matrix is None:
            return
        # generate toplevel window
        self.matrix_window = MatrixWindow(self, matrix=matrix)
        # make window on top of all windows
        self.matrix_window.attributes("-topmost", True)
        # set on close event
        self.matrix_window.protocol("WM_DELETE_WINDOW", lambda: self.hide_matrix())
        # show window
        self.matrix_window.mainloop()

    def hide_matrix(self):
        self.button.configure(state="normal")
        if self.is_matrix_window_open:
            self.matrix_window.destroy()
            self.is_matrix_window_open = False

    def show_matrix(self):
        self.button.configure(state="disabled")
        if not self.is_matrix_window_open:
            self.is_matrix_window_open = True
            self.create_matrix(graph_state.graph)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.label.place(x=self._current_width - self.border_width, y=0)

    def search_path(self):
        self.search_path_event()

    def create_widgets(self):
        self.graph_observer = GraphObserver(self.update_matrix_window)
        graph_state.add_observer(self.graph_observer)

        self.label = Typography(self, text="Tools", type=TextType.h1)
        self.label.pack(side="top", pady=10, anchor="w", padx=10)

        self.number_of_nodes_entry = Input(
            self, "Number of nodes", str(const.DEFAULT_NUMBER_OF_NODES), rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(self.number_of_nodes_change_event)

        self.probability_entry = Input(self, "Probability", str(const.DEFAULT_PROBABILITY), rules=probability_rules)
        self.probability_entry.on_change(self.probability_change_event)
        self.probability_entry.pack(anchor="w", padx=10, fill="x")

        self.button = ctk.CTkButton(self, text="Show Matrix", command=self.show_matrix)
        self.button.pack(padx=10, pady=10, fill="x")

        self.search_path_button = ctk.CTkButton(self, text="Search path", command=self.search_path)
        self.search_path_button.pack(padx=10, fill="x")
