import ttkbootstrap as ttk
from tkinter.font import Font
from src.graph.GraphMatrix import GraphMatrix
from abc import abstractmethod
from src.Theme import theme


class GraphDetailsTab(ttk.Canvas):
    def __init__(self, parent, width=300, height=300, scrollable=True, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.width = width
        self.height = height
        self.scrollable = scrollable
        if scrollable:
            self.scrollbar_y = ttk.Scrollbar(self, orient='vertical')
            self.scrollbar_y.pack(side='right', fill='y')
            self.scrollbar_y.configure(command=self.yview)

            # Add horizontal scrollbar
            self.scrollbar_x = ttk.Scrollbar(self, orient='horizontal')
            self.scrollbar_x.pack(side='bottom', fill='x')
            self.scrollbar_x.configure(command=self.xview)

            self.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
            
            self.bind('<Control-MouseWheel>', self._on_mousewheel_x)
            self.bind("<Configure>", self._on_configure)

        self.configure(scrollregion=(0,0, self.width, self.height))
        self.configure(bg=theme.get('bg'))
        self.configure(highlightthickness=0)

    def _on_configure(self, event):
        if self.height > self.winfo_height():
            self.height = self.height
            self.bind('<MouseWheel>', self._on_mousewheel)
            self.scrollbar_y.pack(fill='y', side='right')
        else:
            self.height = self.winfo_height()
            self.unbind('<MouseWheel>')
            self.scrollbar_y.pack_forget()

        if self.width > self.winfo_width():
            self.width = self.width
            self.bind('<Control-MouseWheel>', self._on_mousewheel_x)
            self.scrollbar_x.pack(fill='x', side='bottom')
        else:
            self.width = self.winfo_width()
            self.unbind('<Control-MouseWheel>')
            self.scrollbar_x.pack_forget()

    def _on_mousewheel_x(self, event):
        self.xview_scroll(-int(event.delta / 120), 'units')
    
    def _on_mousewheel(self, event):
        self.yview_scroll(-int(event.delta / 120), 'units')

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update_wideget(self, matrix: GraphMatrix):
        pass


class CanvasMatrix(GraphDetailsTab):
    def __init__(
            self, parent, root, matrix: GraphMatrix, gap: int = 10, cell_height: int = 20, scrollable=True,
            *args, **kwargs):
        self.root = root
        self.matrix: GraphMatrix = matrix
        self.font = Font(size=16)
        self.gap = gap
        self.cell_height = cell_height + gap
        self.label_start_cell = 1
        self.tab_cell_height = 1
        self.gap_cell = 1
        self.setup_matrix_size()
        super().__init__(parent, scrollable=scrollable, *args, **kwargs)

    def setup_matrix_size(self) -> tuple[int, int]:
        self.longest_string = self.get_longest_string_from_matrix(self.matrix)
        self.cell_width = self.font.measure(self.longest_string) + self.gap

        self.width = (self.matrix.number_of_nodes + self.label_start_cell + self.gap_cell) * self.cell_width
        self.height = (
            self.matrix.number_of_nodes + self.label_start_cell + self.tab_cell_height + self.gap_cell) * self.cell_height

        self.width = self.width + 16
        self.height = self.height + 16

        return self.width, self.height

    def draw(self):
        width, height = self.setup_matrix_size()
        self.delete("all")
        self.draw_labels()
        self.draw_values()

        if hasattr(self, "padding_rect") and self.padding_rect:
            self.delete(self.padding_rect)

        self.padding_rect = self.create_rectangle(0, 0, width, height, fill="", outline="")
        self.configure(scrollregion=self.bbox("all"))
        self._on_configure(None)

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
                             text=str(i), font=self.font, fill=theme.get('primary'))

            y = (i + self.label_start_cell) * self.cell_height
            self.create_text(self.cell_width / 2, (y + (y + self.cell_height)) / 2,
                             text=str(i), font=self.font, fill=theme.get('primary'))

    def draw_values(self):
        for i in range(self.matrix.number_of_nodes):
            for j in range(self.matrix.number_of_nodes):
                x1 = (j + self.label_start_cell) * self.cell_width
                y1 = (i + self.label_start_cell) * self.cell_height
                x2 = x1 + self.cell_width
                y2 = y1 + self.cell_height

                self.create_rectangle(x1, y1, x2, y2, fill=theme.get('bg'), outline=theme.get('light'))
                self.create_text(
                    (x1 + x2) / 2, (y1 + y2) / 2, text=self.matrix.matrix[i][j],
                    font=self.font, fill=theme.get('light'))

    def update_wideget(self, matrix: GraphMatrix):
        self.matrix = matrix
