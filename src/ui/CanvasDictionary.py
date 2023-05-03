from src.ui.Matrix import GraphDetailsTab
from src.graph.GraphModel import GraphMatrix
from tkinter.font import Font
from src.Theme import theme


class CanvasDictionary(GraphDetailsTab):
    def __init__(self, parent, matrix: GraphMatrix, margin_x=10, margin_y=20,  *args, **kwargs):
        self.font = Font(size=16)
        self.dictionary = matrix.get_graph_dictionary()
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.tab_margin = 40
        width, height = self.setup_matrix_size(self.dictionary)
        super().__init__(parent, width, height, *args, **kwargs)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def setup_matrix_size(self, dict) -> tuple[int, int]:
        self.longest_string = self.get_longest_string(dict)
        self.width = self.font.measure(self.longest_string)
        self.height = (self.font.metrics('linespace') + self.font.metrics('descent')) * len(dict) + self.tab_margin
        return self.width, self.height

    def update_wideget(self, matrix: GraphMatrix):
        self.dictionary = matrix.get_graph_dictionary()
        self.setup_matrix_size(self.dictionary)

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
                             text=f"{key}", anchor='nw', font=self.font, fill=theme.get('primary'))
            self.create_text(key_width + self.margin_x + 2, i * self.margin_y,
                             text=f"= {self.dictionary[key]}", anchor='nw', font=self.font, fill=theme.get('light'))

    def draw(self):
        self.draw_dictionary()
