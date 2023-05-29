import ttkbootstrap as ttk
from src.Theme import theme
from src.ui.Menu.Menu import Menu
from src.graph.GraphModel import GraphModel
from src.inputs.Input import Input
from src.utils.validate.rules import Is_number, Min, Max, Is_positive
# from src.ui.Typography import Typography, TextType
from src.state.GraphConfigState import graph_config_state
from src.state.GraphState import graph_state
import src.constance as const
from src.graph.GraphModel import Tree
from src.graph.GraphController import GraphController

number_of_nodes_rules = {
    "is_positive": Is_positive(),
    "is_number": Is_number(),
    "min": Min(1),
    "max": Max(const.MAX_NODE_COUNT),
}

class TreeMenu(Menu):
    def __init__(self, parent, root, controller: GraphController, border_width = 2, **kwargs):
        super().__init__(parent, controller, **kwargs)
        self.border_width = border_width
        self.root = root
        self.create_widgets()

        self.border = ttk.Label(self, text="", width=self.border_width, foreground=theme.get("primary"))

        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        self.border.place(relx=1, relheight=1, width=self.border_width, y=0)

    def set_input_value(self, value: str):
        self.puffer_code_value_label.configure(text=value)

    def init(self):
        if not isinstance(graph_state.get(), Tree):
            self.set_input_value("Not a tree")
        # get puffer code from graph
        if hasattr(self.graph_model, "get_pruffer_code"):
            self.set_input_value(self.graph_model.get_pruffer_code(self.graph_model.matrix))

    def on_graph_state_change(self, graph: GraphModel):
        self.init()

    def create_widgets(self):
        self.number_of_nodes_entry = Input(
            self, "Number of nodes", str(const.DEFAULT_NUMBER_OF_NODES), rules=number_of_nodes_rules)
        self.number_of_nodes_entry.on_change(lambda e: graph_config_state.set_number_of_nodes(int(e)))

        self.puffer_code_label = ttk.Label(self, text="Puffer code")
        self.puffer_code_label.pack(padx=10, pady=10, fill="x")

        self.puffer_code_value_label = ttk.Label(self, text="Puffer code value")
        self.puffer_code_value_label.pack(padx=10, fill="x")

        # self.button = ctk.CTkButton(self, text="Show Graph Details", command=self.show_matrix)
        # self.button.pack(padx=10, pady=10, fill="x")

        self.generate_graph_button = ttk.Button(
            self, text="Generate tree", command=lambda e=graph_config_state.get(): self.generate_graph_event(e), cursor="hand2")
        self.generate_graph_button.pack(padx=10, pady=10, fill="x")

        graph_state.subscribe(self.on_graph_state_change)    
