from src.ui.windows.TopLevelWindow import TopLevelWindow
from src.graph.Graph import Graph
from src.ui.Matrix import CanvasMatrix, GraphDetailsTab
from src.ui.CanvasDictionary import CanvasDictionary
from src.utils.Event import Event
import customtkinter as ctk


class GraphDeatails(TopLevelWindow):
    def __init__(self, master, graph: Graph, start_tab: str = "Matrix", *args, **kwargs):
        super().__init__(master, title="Graph Details", *args, **kwargs)
        self._min_width = 300
        self._min_height = 300
        self.graph = graph
        self.tab_change_event = Event()
        self.tab_view = ctk.CTkTabview(self)
        self.start_tab = start_tab
        self.tab_view.add('Matrix')
        self.tab_view.add('Wages Matrix')
        self.tab_view.add('Dictionary')
        self.tab_view.set(self.start_tab)
        # Graph matrix
        self.matrix_widget: GraphDetailsTab = CanvasMatrix(
            parent=self.tab_view.tab('Matrix'), matrix=graph.get_matrix())
        self.matrix_widget.pack(fill='both', expand=True)
        self.matrix_widget.draw()
        # Wages matrix
        self.wages_matrix_widget: GraphDetailsTab = CanvasMatrix(
            parent=self.tab_view.tab('Wages Matrix'), matrix=graph.get_wages())
        self.wages_matrix_widget.pack(fill='both', expand=True)
        self.wages_matrix_widget.draw()
        # Dictionary
        self.dictionary_widget: GraphDetailsTab = CanvasDictionary(
            parent=self.tab_view.tab('Dictionary'), matrix=graph.get_matrix())
        self.dictionary_widget.pack(fill='both', expand=True)
        self.tab_view.pack(fill='both', expand=True, anchor='w')
        self.tab_view.configure(command=self.on_tab_change_event)
        self.on_tab_change_event()

    def on_tab_change(self, cb):
        self.tab_change_event += cb

    def off_tab_change(self, cb):
        self.tab_change_event -= cb

    def update_matrix_widegt(self):
        self.matrix_widget.update_wideget(self.graph.get_matrix())
        self.matrix_widget.draw()

    def update_wages_matrix_widegt(self):
        self.wages_matrix_widget.update_wideget(self.graph.get_wages())
        self.wages_matrix_widget.draw()

    def update_dictionary_widegt(self):
        self.dictionary_widget.update_wideget(self.graph.get_matrix())
        self.dictionary_widget.draw()

    def on_tab_change_event(self):
        current_active_tab: str = self.tab_view.get()

        if current_active_tab == 'Matrix':
            self.update_matrix_widegt()
        elif current_active_tab == 'Wages Matrix':
            self.update_wages_matrix_widegt()
        elif current_active_tab == 'Dictionary':
            self.update_dictionary_widegt()

        self.update_window_size()

    def update_window_size(self):
        width = max(self.matrix_widget.width, self.wages_matrix_widget.width, self.dictionary_widget.width)
        height = max(self.matrix_widget.height, self.wages_matrix_widget.height, self.dictionary_widget.height)

        if width < self._min_width:
            width = self._min_width
        if height < self._min_height:
            height = self._min_height

        self.geometry('%dx%d+%d+%d' % (width, height, self.winfo_x(), self.winfo_y()))

    def update_graph(self, graph: Graph):
        self.graph = graph
        self.on_tab_change_event()

    def destroy(self):
        super().destroy()
