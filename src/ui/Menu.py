import customtkinter as ctk
from src.utils.Event import Event


class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        ctk.CTkFrame.__init__(self, parent)
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

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Tools")
        self.label.pack(side="top", fill="x", pady=10)

        number_of_nodes = ctk.StringVar()
        number_of_nodes.trace("w", lambda name, index, mode,
                              sv=number_of_nodes: self.number_of_nodes_change_event(number_of_nodes))

        probability = ctk.StringVar()
        probability.trace("w", lambda name, index, mode, sv=probability: self.probability_change_event(probability))

        self.number_of_nodes_label = ctk.CTkLabel(self, text="Number of nodes")
        self.number_of_nodes_entry = ctk.CTkEntry(self, textvariable=number_of_nodes)

        self.number_of_nodes_label.pack(padx=10, pady=5, anchor="w")
        self.number_of_nodes_entry.pack(padx=10)

        self.probability_label = ctk.CTkLabel(self, text="Probability")
        self.probability_entry = ctk.CTkEntry(self, textvariable=probability)

        self.probability_label.pack(padx=10, pady=5, anchor="w")
        self.probability_entry.pack(padx=10)

        self.generate_button = ctk.CTkButton(self, text="Generate graph")
        self.generate_button.pack(padx=10, pady=10)
