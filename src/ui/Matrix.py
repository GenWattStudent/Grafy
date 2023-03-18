import customtkinter as ctk
from src.graph.GraphMatrix import GraphMatrix


class Matrix(ctk.CTkCanvas):
    def __init__(self, parent, matrix: GraphMatrix | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.matrix: GraphMatrix | None = matrix
        self.square_size = 20
        self.gap = 25
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def draw(self):
        if self.matrix is None:
            return
        self.delete("all")
        self.draw_matrix()
        self.draw_values()

    def draw_matrix(self):
        if self.matrix is None:
            return
        half_gap = self.gap / 2
        matrix_size = self.matrix.number_of_nodes * self.square_size + half_gap
        self.create_line(half_gap, half_gap, half_gap, matrix_size, fill="white", width=1)
        self.create_line(matrix_size, half_gap, matrix_size, matrix_size, fill="white", width=1)

    def draw_values(self):
        if self.matrix is None:
            return
        for i in range(self.matrix.number_of_nodes):
            for j in range(self.matrix.number_of_nodes):
                x = i * self.square_size + self.gap
                y = j * self.square_size + self.gap
                self.create_text(x, y, text=self.matrix[i][j], fill="white")

    def update_wideget(self, matrix: GraphMatrix):
        self.matrix = matrix
        self.draw()
