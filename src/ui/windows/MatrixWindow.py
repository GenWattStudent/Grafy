from src.ui.windows.TopLevelWindow import TopLevelWindow
from src.graph.GraphMatrix import GraphMatrix
from src.ui.Matrix import Matrix


class MatrixWindow(TopLevelWindow):
    def __init__(self, master, matrix: GraphMatrix, *args, **kwargs):
        super().__init__(master, title="Matrix", *args, **kwargs)
        self._min_width = 300
        self._min_height = 300
        self.matrix_widget = Matrix(self, matrix)
        self.matrix_widget.draw()
        self.matrix_widget.pack(pady=10, padx=10, fill="both", expand=True)
        self.update_window_size()

    def update_window_size(self):
        if self.matrix_widget.matrix is not None:
            x, y = 300, 300
            width = self.matrix_widget.matrix.number_of_nodes * self.matrix_widget.square_size + self.matrix_widget.gap
            height = self.matrix_widget.matrix.number_of_nodes * self.matrix_widget.square_size + self.matrix_widget.gap
            if width < self._min_width:
                width = self._min_width
            if height < self._min_height:
                height = self._min_height
            self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def update_matrix(self, matrix: GraphMatrix):
        self.update_window_size()
        self.matrix_widget.update_wideget(matrix)
        self.matrix_widget.draw()
