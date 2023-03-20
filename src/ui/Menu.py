import customtkinter as ctk
from src.utils.Event import Event
from src.inputs.Input import Input
from src.utils.validate.rules import Is_number, Min, Max, Is_float, Is_positive
from src.ui.Typography import Typography, TextType
from src.state.GraphConfigState import graph_config_state
from src.state.GraphState import graph_state
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
        self.search_path_event = Event()
        self.generate_graph_event = Event()
        self.border_width = 2
        self.is_matrix_window_open = False
        self.create_widgets()

        self.label = ctk.CTkLabel(self, text="", width=self.border_width, height=const.SCREEN_HEIGHT, fg_color="white")

    def on_search_path(self, cb):
        self.search_path_event += cb

    def off_search_path(self, cb):
        self.search_path_event -= cb

    def on_generate_graph(self, cb):
        self.generate_graph_event += cb

    def off_generate_graph(self, cb):
        self.generate_graph_event -= cb

    def update_matrix_window(self, matrix: GraphMatrix, prev_matrix: GraphMatrix):
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
            self.matrix_window = None
            self.is_matrix_window_open = False

    def show_matrix(self):
        self.button.configure(state="disabled")
        if not self.is_matrix_window_open:
            self.is_matrix_window_open = True
            self.create_matrix(graph_state.get())

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.label.place(x=self._current_width - self.border_width, y=0)

    def search_path(self):
        self.search_path_event()

    def toogle_intersection(self):
        graph_config_state.set_is_show_intersections(not graph_config_state.get_is_show_intersections())

    def create_widgets(self):
        graph_state.subscribe(self.update_matrix_window)

        self.label = Typography(self, text="Tools", type=TextType.h1)
        self.label.pack(side="top", pady=10, anchor="w", padx=10)

        self.number_of_nodes_entry = Input(
            self, "Number of nodes", str(const.DEFAULT_NUMBER_OF_NODES), rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(lambda e: graph_config_state.set_number_of_nodes(int(e)))

        self.probability_entry = Input(self, "Probability", str(const.DEFAULT_PROBABILITY), rules=probability_rules)
        self.probability_entry.on_change(lambda e: graph_config_state.set_probability(float(e)))
        self.probability_entry.pack(anchor="w", padx=10, fill="x")

        self.intersection_checkbox = ctk.CTkCheckBox(self, text="Intersection", command=self.toogle_intersection)
        self.intersection_checkbox.pack(anchor="w", padx=10, pady=10)

        self.button = ctk.CTkButton(self, text="Show Matrix", command=self.show_matrix)
        self.button.pack(padx=10, pady=10, fill="x")

        self.search_path_button = ctk.CTkButton(self, text="Search path", command=self.search_path)
        self.search_path_button.pack(padx=10, fill="x")

        self.generate_graph_button = ctk.CTkButton(
            self, text="Generate graph", command=lambda e=graph_config_state.get(): self.generate_graph_event(e))
        self.generate_graph_button.pack(padx=10, pady=10, fill="x")
