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
from src.utils.Simulation import Simulation
from src.algorithms.SearchAlgorithms import SearchAlgorithms

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
        self.density_text_var = tkk.StringVar(value="Density: 0.0")
        self.intersection_text_var = tkk.StringVar(value="Intersection: Off")
        self.number_of_cycles_text_var = tkk.StringVar(value="Number of cycles: 0")
        self.path_distance_text_var = tkk.StringVar(value="Path distance: None")
        self.is_directed_checkbox_var = tkk.BooleanVar(value=False)
        self.create_widgets()

        self.bind("<Configure>", self.on_resize)

    def simulate(self, simulation: Simulation):
        self.simulation_frame = tkk.Frame(self)
        self.simulation_frame.pack(fill="both", expand=True)
        self.prev_button = tkk.Button(self.simulation_frame, text="Prev", command=simulation.previous, cursor="hand2")
        self.prev_button.pack(side="left", padx=10, pady=10)
        self.next_button = tkk.Button(self.simulation_frame, text="Next", command=simulation.next, cursor="hand2")
        self.next_button.pack(side="right", padx=10, pady=10)

    def destroy_simulate(self):
        self.simulation_frame.destroy()

    def on_resize(self, event):
        self.option_info.configure(wraplength=self.winfo_width() - 10)
        self.isomophic_label.configure(wraplength=self.winfo_width() - 10)

    def update_matrix_window(self, graph: GraphModel):
        if hasattr(self, "matrix_window") and self.matrix_window is not None:
            return self.matrix_window.update_graph(graph)

    def create_matrix(self, graph: GraphModel):
        # generate toplevel window
        self.matrix_window = GraphDeatails(self.root, graph=graph)
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
            self.create_matrix(graph_state.get())

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

    def set_density_text(self, density: float):
        self.density_text_var.set(f"Density: {round(density, 2)}")

    def update_graph_info(self, graph_model: GraphModel):
        self.set_density_text(graph_model.density)
        self.number_of_cycles_text_var.set(f"Number of cycles: {SearchAlgorithms().count_cycles(graph_model.get_graph_dictionary()) // 2}")
        if graph_model.config.is_show_intersections:
            self.intersection_text_var.set(f"Intersection: {len(graph_model.intersections)}")
        else:
            self.intersection_text_var.set(f"Intersection: off")

        if graph_model.path_distance is not None:
            self.path_distance_text_var.set(f"Path distance: {graph_model.path_distance}")
        else:
            self.path_distance_text_var.set(f"Path distance: None")

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

        self.intersection_checkbox = tkk.Checkbutton(self, text="Show Intersections", command=self.toogle_intersection, variable=tkk.BooleanVar(value=False))
        self.intersection_checkbox.pack(anchor="w", padx=10, pady=10)

        self.is_directed_checkbox = tkk.Checkbutton(self, text=f"Directed", command= lambda: self.controller.directed(self.is_directed_checkbox_var.get()), variable=self.is_directed_checkbox_var)
        self.is_directed_checkbox.pack(anchor="w", padx=10, pady=10)
 
        self.info_frame = tkk.Frame(self)
        self.info_frame.pack(anchor="w", padx=10, pady=10, fill="x")

        self.density_label = Typography(self.info_frame, textvariable=self.density_text_var)
        self.density_label.pack(anchor="w")

        self.number_of_cycles_label = Typography(self.info_frame, textvariable=self.number_of_cycles_text_var)
        self.number_of_cycles_label.pack(anchor="w")

        self.intersection_label = Typography(self.info_frame, textvariable=self.intersection_text_var)
        self.intersection_label.pack(anchor="w")  

        self.path_distance_label = Typography(self.info_frame, textvariable=self.path_distance_text_var)
        self.path_distance_label.pack(anchor="w")

        self.isomophic_label = Typography(self.info_frame, textvariable=self.isomorphic_var)
        self.isomophic_label.pack(anchor="w", fill="x")

        self.option = tkk.Combobox(self, values=["BFS", "Dijkstra", "DFS"], state="readonly")
        self.option.current(0)
        self.option.bind("<<ComboboxSelected>>", self.algorithm_change)
        self.option.pack(anchor="w", padx=10, pady=10, fill="x")

        self.option_info = Typography(self, text=self.get_node_count_message())
        self.option_info.pack(anchor="w", padx=10)

        self.button = tkk.Button(self, text="Show Graph Details", command=self.show_matrix, cursor="hand2")
        self.button.pack(padx=10, pady=10, fill="x")

        self.search_path_button = tkk.Button(self, text="Search path", command=self.search_path, cursor="hand2")
        self.search_path_button.pack(padx=10, fill="x")

        self.generate_graph_button = tkk.Button(
            self, text="Generate graph", command=lambda e=graph_config_state.get(): self.generate_graph_event(e), cursor="hand2")
        self.generate_graph_button.pack(padx=10, pady=10, fill="x")

        graph_state.subscribe(self.update_matrix_window)
        graph_state.subscribe(self.update_graph_info)
