from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController
from src.ui.windows.TopLevelWindow import TopLevelWindow
from src.ui.Typography import Typography
from reportlab.lib.pagesizes import A4
from PIL import ImageGrab
from src.inputs.Input import Input
from tkinter.filedialog import asksaveasfilename
from src.graph.GraphMatrix import GraphMatrix
from src.graph.GraphModel import GraphModel
from src.utils.Event import Event
from src.state.AlgorithmState import algorithm_state
from src.algorithms.SearchAlgorithms import SearchAlgorithms
from src.utils.PDFBuilder import PDFBuilder
import ttkbootstrap as tkk
import uuid

class Raport(TopLevelWindow):
    def __init__(self, parent, title: str, controller: GraphController, **kwargs):
        super().__init__(parent, title, **kwargs)
        self.parent = parent
        self.controller = controller
        self.min_width = 400
        self.file_name_var = tkk.StringVar(value=str(uuid.uuid4()))
        self.is_graph_image = tkk.BooleanVar(value=True)
        self.is_matrix = tkk.BooleanVar(value=True)
        self.is_graph_details = tkk.BooleanVar(value=True)
        self.is_dict = tkk.BooleanVar(value=True)
        self.is_bfs_output = tkk.BooleanVar(value=True)
        self.is_bfs_layers = tkk.BooleanVar(value=True)
        self.pdf_builder = PDFBuilder(self.file_name_var.get() + ".pdf", pagesize=A4)
        self.destroy_event = Event()
        self.create_widgets()
    
    def create_temp_canvas_img(self):
        x = self.controller.view.winfo_rootx() + self.controller.view.winfo_x()
        y = self.controller.view.winfo_rooty() + self.controller.view.winfo_y()
        x1 = x + self.controller.view.winfo_width()
        y1 = y + self.controller.view.winfo_height()
        image = ImageGrab.grab().crop((x, y, x1, y1))

        return image

    def on_destroy(self, cb):
        self.destroy_event += cb
    
    def off_destroy(self, cb):
        self.destroy_event -= cb
    
    def remove_temp(self, path: str):
        import os
        os.remove(path)
    
    def draw_matrix(self, matrix: GraphMatrix):
        self.pdf_builder.add_header_2('Graph Matrix')
        rows = str(matrix).split("\n")
        for row in rows:
             self.pdf_builder.add_body(row)
    
    def draw_graph_details(self, graph: GraphModel):
        self.pdf_builder.add_header_2('Graph Details')
        self.pdf_builder.add_body(f'Degrees sum: {len(graph.edges) * 2}')
        self.pdf_builder.add_body(f'Edges: {len(graph.edges)}')
        self.pdf_builder.add_body(f'Density: {round(graph.density, 2)}')
        self.pdf_builder.add_body(f'Nodes: {len(graph.nodes)}')

    def draw_dict(self, dict: dict[int, list[int]]):
        for key, value in dict.items():
            self.pdf_builder.add_body(f'{key}: {value}')

    def prepare_report(self):
        img = self.create_temp_canvas_img()
       
        self.pdf_builder.setTitle(f'Graph raport {self.file_name_var.get()}')

        if self.pdf_main_header_input.get() == "":
            self.pdf_builder.add_header_1(f'Graph Raport')
        else:
            self.pdf_builder.add_header_1(self.pdf_main_header_input.get())

        model = self.controller.current_graph.get()
        if self.is_matrix.get():
            self.draw_matrix(model.matrix)
        # dictionary
        dict = model.get_graph_dictionary()
        if self.is_dict.get():
            self.pdf_builder.add_header_2('Graph Dictionary')
            self.draw_dict(dict)
            selected_nodes: list[] = model.get_nodes_from_list(model.selected_elements)
        if len(selected_nodes) > 0 and len(selected_nodes) == algorithm_state.get_search_algorithm().min_selected_nodes:
            search_algorithms = SearchAlgorithms()
            
            bfs_dict = search_algorithms.bfs(dict, selected_nodes[0])
            # bfs output
            if self.is_bfs_output.get():
                self.pdf_builder.add_header_2('BFS Output')
                self.draw_dict(bfs_dict)
            # dfs layer
            if self.is_bfs_layers.get():
                bfs_layers = search_algorithms.get_layers_from_bfs_output(bfs_dict, selected_nodes[0].index - 1)
                self.pdf_builder.add_header_2('BFS Layers')
                for layer, vertices in bfs_layers:
                    self.pdf_builder.add_body(f'Layer {layer + 1}: {vertices}')

        if self.is_graph_details.get():
            self.draw_graph_details(model)

        if self.is_graph_image.get():
            self.pdf_builder.add_image(img)

    def get_report(self, temp: bool = False) -> str:
        if temp == False:
            file_path = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")], initialfile=self.file_name_var.get())
            self.destroy_event()
            if file_path == "": return ''

            full_file_path = file_path if file_path.endswith(".pdf") else f"{file_path}.pdf"
            self.pdf_builder.set_filename(full_file_path)
            self.destroy()
        else:
            full_file_path = "temp.pdf"

        self.prepare_report()
        self.pdf_builder.build()
        self.pdf_builder.save()

        return full_file_path

    def handle_change(self, value: str):
        self.file_name_var.set(value)
        self.file_name_input.config(width=len(value) + 5)

        if self.min_width < len(value) * 10:
            self.min_width = len(value) * 10
    
    def destroy_window(self) -> None:
        self.destroy_event()
        self.destroy()

    def create_widgets(self):
        self.header = Typography(self, text="Get Raport PDF", font=("Helvetica-Bold", 28))
        self.header.pack(pady=10)

        self.form_frame = tkk.Frame(self)
        self.form_frame.pack(pady=10, expand=True, fill="x")

        self.file_name_input = Input(self.form_frame, default_value=self.file_name_var.get(), label_text="File name")
        self.file_name_input.on_change(self.handle_change)
        self.file_name_input.pack(pady=5)
        self.file_name_input.focus()
        self.handle_change(self.file_name_var.get())

        self.pdf_main_header_input = Input(self.form_frame, default_value="Graph Raport", label_text="Main header")
        self.pdf_main_header_input.pack(pady=5)

        self.image_checkbox = tkk.Checkbutton(self.form_frame, text="Graph Image", variable=self.is_graph_image, cursor="hand2")
        self.image_checkbox.pack(side="left", pady=5, padx=10)

        self.matrix_checkbox = tkk.Checkbutton(self.form_frame, text="Graph Matrix", variable=self.is_matrix, cursor="hand2")
        self.matrix_checkbox.pack(side="left", pady=5, padx=10)

        self.dict_checkbox = tkk.Checkbutton(self.form_frame, text="Graph Dictionary", variable=self.is_dict, cursor="hand2")
        self.dict_checkbox.pack(side="left", pady=5, padx=10)

        self.form_frame2 = tkk.Frame(self)
        self.form_frame2.pack(pady=10, expand=True, fill='x')

        self.bfs_output_checkbox = tkk.Checkbutton(self.form_frame2, text="BFS Output", variable=self.is_bfs_output, cursor="hand2")
        self.bfs_output_checkbox.pack(side='left', pady=5, padx=10)

        self.bfs_layers_checkbox = tkk.Checkbutton(self.form_frame2, text="BFS Layers", variable=self.is_bfs_layers, cursor="hand2")
        self.bfs_layers_checkbox.pack(side='left', pady=5, padx=10)

        self.graph_details_checkbox = tkk.Checkbutton(self.form_frame2, text="Graph Details", variable=self.is_graph_details, cursor="hand2")
        self.graph_details_checkbox.pack(side='left', pady=5, padx=10)

        self.action_button_frame = tkk.Frame(self)
        self.action_button_frame.pack(pady=10)

        self.get_report_button = tkk.Button(self.action_button_frame, text="Get Raport", command=self.get_report, cursor="hand2")
        self.get_report_button.pack(side="left", padx=10)

        self.cancle_button = tkk.Button(self.action_button_frame, text="Cancle", command=self.destroy_window, style="Danger.TButton", cursor="hand2")
        self.cancle_button.pack(side="left", padx=10)