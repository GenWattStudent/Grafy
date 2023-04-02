import customtkinter as ctk
from src.graph.GraphMatrix import GraphMatrix
from abc import abstractmethod


class GraphDetailsTab(ctk.CTkCanvas):
    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.width = width
        self.height = height

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update_wideget(self, matrix: GraphMatrix):
        pass


class CanvasMatrix(GraphDetailsTab):
    def __init__(
            self, parent, matrix: GraphMatrix, gap: int = 10, cell_height: int = 20,
            *args, **kwargs):
        self.matrix: GraphMatrix = matrix
        self.font = ctk.CTkFont(size=16)
        self.gap = gap
        self.cell_height = cell_height + gap
        self.label_start_cell = 1
        self.tab_cell_height = 1
        self.gap_cell = 1
        width, height = self.setup_matrix_size()
        super().__init__(parent, width, height, *args, **kwargs)
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def setup_matrix_size(self) -> tuple[int, int]:
        self.longest_string = self.get_longest_string_from_matrix(self.matrix)
        self.cell_width = self.font.measure(self.longest_string) + self.gap

        self.width = (self.matrix.number_of_nodes + self.label_start_cell + self.gap_cell) * self.cell_width
        self.height = (
            self.matrix.number_of_nodes + self.label_start_cell + self.tab_cell_height + self.gap_cell) * self.cell_height

        return self.width, self.height

    def draw(self):
        self.setup_matrix_size()
        self.delete("all")
        self.draw_labels()
        self.draw_values()

    def get_longest_string_from_matrix(self, matrix: GraphMatrix):
        longest_string = ''
        for i in range(matrix.number_of_nodes):
            for j in range(matrix.number_of_nodes):
                if len(str(matrix.matrix[i][j])) > len(longest_string):
                    longest_string = str(matrix.matrix[i][j])
                if len(longest_string) < len(str(i)):
                    longest_string = str(i)
        return longest_string

    def draw_labels(self):
        for i in range(self.matrix.number_of_nodes):
            x = (i + self.label_start_cell) * self.cell_width
            self.create_text((x + (x + self.cell_width)) / 2, self.cell_height / 2,
                             text=str(i), font=self.font, fill="yellow")

            y = (i + self.label_start_cell) * self.cell_height
            self.create_text(self.cell_width / 2, (y + (y + self.cell_height)) / 2,
                             text=str(i), font=self.font, fill="yellow")

    def draw_values(self):
        for i in range(self.matrix.number_of_nodes):
            for j in range(self.matrix.number_of_nodes):
                x1 = (j + self.label_start_cell) * self.cell_width
                y1 = (i + self.label_start_cell) * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height

                self.create_rectangle(x1, y1, x2, y2, fill="#2b2b2b", outline="white")
                self.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2, text=self.matrix.matrix[i][j],
                    font=self.font, fill="white")

    def update_wideget(self, matrix: GraphMatrix):
        self.matrix = matrix
