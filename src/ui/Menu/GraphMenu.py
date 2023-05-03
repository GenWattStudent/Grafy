import ttkbootstrap as tkk
import src.constance as const
from src.state.AlgorithmState import algorithm_state
from src.state.GraphConfigState import graph_config_state
from src.state.GraphState import graph_state
from src.graph.GraphModel import GraphModel
from src.ui.Menu.Menu import Menu
from src.ui.Typography import Typography
from src.ui.windows.GraphDetails import GraphDeatails
from src.inputs.Input import Input
from src.graph.GraphController import GraphController
from src.utils.validate.rules import Is_number, Min, Max, Is_float, Is_positive

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


class GraphMenu(Menu):
    def __init__(self, parent, root, controller: GraphController, border_width = 2,**kwargs):
        super().__init__(parent, controller, **kwargs)
        self.is_matrix_window_open = False
        self.border_width = border_width
        self.root = root
        self.create_widgets()

        self.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.option_info.configure(wraplength=self.winfo_width() - 10)

    def update_matrix_window(self, graph: GraphModel):
        if hasattr(self, "matrix_window") and self.matrix_window is not None:
            return self.matrix_window.update_graph(graph)

    def create_matrix(self, graph: GraphModel):
        # generate toplevel window
        self.matrix_window = GraphDeatails(self.root, graph=graph_state.get())
        # make window on top of all windows
        self.matrix_window.attributes("-topmost", True)
        # set on close event
        self.matrix_window.protocol("WM_DELETE_WINDOW", lambda: self.hide_matrix())
        # show window
        self.matrix_window.mainloop()

    def get_node_count_message(self) -> str:
        return f"Select {algorithm_state.get_search_algorithm().min_selected_nodes} nodes by clicking on them to start search"

    def hide_matrix(self):
        self.button.configure(state="normal")
        if self.is_matrix_window_open and self.matrix_window:
            self.matrix_window.destroy()
            self.matrix_window = None
            self.is_matrix_window_open = False

    def show_matrix(self):
        self.button.configure(state="disabled")
        if not self.is_matrix_window_open:
            self.is_matrix_window_open = True
            self.create_matrix(self.graph_model)

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.root.update()

    def search_path(self):
        self.search_path_event()

    def algorithm_change(self, event):
        algorithm_state.set_search_algorithm(event.widget.get())
        self.option_info.configure(text=self.get_node_count_message())

    def toogle_intersection(self):
        graph_config_state.set_is_show_intersections(not graph_config_state.get_is_show_intersections())

    def probability_filtr(self, value: str) -> str:
        return value.replace(",", ".")

    def update_graph_info(self, graph_model: GraphModel):
        self.density_label.configure(text=f"Density: {round(graph_model.density, 2)}")
        if graph_model.config.is_show_intersections:

            self.intersection_label.configure(text=f"Inersections: {len(graph_model.intersections)}")
        else:
            self.intersection_label.configure(text=f"Inersections: off")

        if graph_model.path_distance is not None:
            self.path_distance_label.configure(text=f"Path distance: {graph_model.path_distance}px")
        else:
            self.path_distance_label.configure(text=f"Path distance: None")

    def destroy(self):
        self.hide_matrix()
        self.density_label.destroy()
        self.intersection_label.destroy()
        self.path_distance_label.destroy()
        super().destroy()

    def create_widgets(self):
        self.number_of_nodes_entry = Input(
            self, "Number of nodes", str(const.DEFAULT_NUMBER_OF_NODES), rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(lambda e: graph_config_state.set_number_of_nodes(int(e)))

        self.probability_entry = Input(
            self, "Probability", str(const.DEFAULT_PROBABILITY),
            rules=probability_rules, filtr=self.probability_filtr)
        self.probability_entry.on_change(lambda e: graph_config_state.set_probability(float(e)))
        self.probability_entry.pack(anchor="w", padx=10, fill="x")

        self.intersection_checkbox = tkk.Checkbutton(self, text="Intersection", command=self.toogle_intersection, variable=tkk.BooleanVar(value=False))
        self.intersection_checkbox.pack(anchor="w", padx=10, pady=10)
 
        self.info_frame = tkk.Frame(self)
        self.info_frame.pack(anchor="w", padx=10, pady=10, fill="x")

        self.density_label = Typography(self.info_frame, text=f"Density: {round(self.graph_model.density, 2)}")
        self.density_label.pack(anchor="w")

        self.intersection_label = Typography(self.info_frame, text=f"Inersections: {len(self.graph_model.intersections)}")
        self.intersection_label.pack(anchor="w")  

        self.path_distance_label = Typography(self.info_frame)
        self.path_distance_label.pack(anchor="w")

        self.option = tkk.Combobox(self, values=["BFS", "Dijkstra", "DFS"], state="readonly")
        self.option.current(0)
        self.option.bind("<<ComboboxSelected>>", self.algorithm_change)
        self.option.pack(anchor="w", padx=10, pady=10, fill="x")

        self.option_info = Typography(self, text=self.get_node_count_message())
        self.option_info.pack(anchor="w", padx=10)

        self.button = tkk.Button(self, text="Show Graph Details", command=self.show_matrix)
        self.button.pack(padx=10, pady=10, fill="x")

        self.search_path_button = tkk.Button(self, text="Search path", command=self.search_path)
        self.search_path_button.pack(padx=10, fill="x")

        self.generate_graph_button = tkk.Button(
            self, text="Generate graph", command=lambda e=graph_config_state.get(): self.generate_graph_event(e))
        self.generate_graph_button.pack(padx=10, pady=10, fill="x")

        graph_state.subscribe(self.update_matrix_window)
        graph_state.subscribe(self.update_graph_info)
