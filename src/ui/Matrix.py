import customtkinter as ctk
from src.graph.GraphMatrix import GraphMatrix


class Matrix(ctk.CTkCanvas):
    def __init__(self, parent, matrix: GraphMatrix | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.matrix: GraphMatrix = matrix
        self.square_size = 20
        self.configure(bg='#2b2b2b')
        self.configure(highlightthickness=0)

    def draw(self):
        if self.matrix is None:
            return
        self.delete("all")
        self.draw_matrix()
        self.draw_values()

    def draw_matrix(self):
        matrix_size = self.matrix.number_of_nodes * self.square_size + 12
        self.create_line(0, 5, 0, matrix_size, fill="white", width=1)
        self.create_line(matrix_size, 5, matrix_size, matrix_size, fill="white", width=1)

    def draw_values(self):
        for i in range(self.matrix.number_of_nodes):
            for j in range(self.matrix.number_of_nodes):
                self.create_text(i * self.square_size + 15, j * self.square_size + 15,
                                 text=self.matrix[i][j], fill="white")

    def update_wideget(self, matrix: GraphMatrix):
        self.matrix = matrix
        self.draw()
