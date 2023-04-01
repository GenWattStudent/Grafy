from src.ui.Matrix import GraphDetailsTab
from src.graph.Graph import GraphMatrix
import customtkinter as ctk


class CanvasDictionary(GraphDetailsTab):
    def __init__(self, parent, matrix: GraphMatrix, margin_x=10, margin_y=20,  *args, **kwargs):
        self.font = ctk.CTkFont(size=16)
        self.dictionary = matrix.get_graph_dictionary()
        self.margin_x = margin_x
        self.margin_y = margin_y
        width, height = self.setup_matrix_size()
        super().__init__(parent, width, height, *args, **kwargs)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def setup_matrix_size(self) -> tuple[int, int]:
        self.longest_string = self.get_longest_string(self.dictionary)
        self.width = self.font.measure(self.longest_string)
        self.height = self.font.metrics('linespace') * len(self.dictionary)

        return self.width, self.height

    def update_wideget(self, matrix: GraphMatrix):
        self.width, self.height = self.setup_matrix_size()
        self.dictionary = matrix.get_graph_dictionary()

    def get_longest_string(self, dictionary) -> str:
        longest_string: str = ""
        for key in dictionary:
            string = f"{key} = {dictionary[key]}"
            if len(string) > len(longest_string):
                longest_string = string

        return longest_string

    def draw_dictionary(self):
        self.delete('all')
        for i, key in enumerate(self.dictionary):
            key_width = self.font.measure(str(key))
            self.create_text(self.margin_x, i * self.margin_y,
                             text=f"{key}", anchor='nw', font=self.font, fill='yellow')
            self.create_text(key_width + self.margin_x + 2, i * self.margin_y,
                             text=f"= {self.dictionary[key]}", anchor='nw', font=self.font, fill='white')

    def draw(self):
        self.draw_dictionary()