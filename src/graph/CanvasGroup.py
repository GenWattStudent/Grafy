from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController
from src.ui.GraphCanvas import GraphCanvas
from src.graph.GraphModel import GraphModel
from src.ui.Toolbar import Tools
import uuid

class CanvasGroup:
    def __init__(self, root, controller: GraphController):
        self.root = root
        self.controller = controller
        self.canvas_list: list[GraphCanvas] = []
    
    def bind_canvas_events(self, canvas: GraphCanvas):
        canvas.bind("<Button-1>", self.controller.on_click)
        canvas.bind("<B1-Motion>", self.controller.on_drag)
        canvas.bind("<Motion>", self.controller.motion)
        canvas.bind("<ButtonRelease-1>", self.controller.on_release)
    
    def on_current_canvas_change(self, canvas: GraphCanvas):
        self.controller.view = canvas
        self.controller.view.set_active(True)
        self.controller.view.canvas_helper.canvas = canvas
        self.controller.toolbar_helper.canvas = canvas
        self.controller.toolbar_helper.canvas_helper.canvas = canvas
        self.controller.drag.canvas = canvas
        self.controller.drag.canvas_helper.canvas = canvas
        self.controller.canvas_helper.canvas = canvas
        self.controller.simulation.view = canvas
        
    def destroy_canvases(self):
        for canvas in self.canvas_list:
            canvas.destroy()
        self.canvas_list.clear()
    
    def create_canvas(self, model: GraphModel) -> GraphCanvas:
        canvas = GraphCanvas(self.root, model)
        canvas.tab_id = model.tab_id
        self.bind_canvas_events(canvas)
        self.canvas_list.append(canvas)
        canvas.pack(side='left', fill='both', expand=True)
        canvas.draw_graph()
        return canvas
    
    def create_canvases(self, graph_models: list[GraphModel]):
        for graph in graph_models:
            self.create_canvas(graph)

    def change_current_canvas(self, canvas_id: uuid.UUID, is_click: bool = False):
        if (canvas_id != self.controller.view.id and self.controller.toolbar.selected_tool.get() != Tools.SELECT) or (is_click and canvas_id != self.controller.view.id):
            for canvas in self.canvas_list:
                if canvas.id == canvas_id:
                    graph = self.controller.graph_sheets.get_graph_by_id(canvas.tab_id)
                    
                    if graph:
                        if self.controller.view.winfo_exists():
                            self.controller.toolbar.deselect_all_tool()
                            self.controller.view.set_active(False)
                            self.controller.graph_sheets.select(graph.tab_id)
                            self.controller.view.draw_graph()
                        
                        self.on_current_canvas_change(canvas)
                        self.controller.current_graph.set(graph)
                        canvas.draw_graph()
                    return
