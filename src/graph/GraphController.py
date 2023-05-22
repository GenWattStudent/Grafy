from __future__ import annotations
from src.graph.GraphModel import GraphModel
from src.ui.GraphCanvas import GraphCanvas
from src.GraphFile import FileManager
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.ui.Toolbar import ToolBar, Tools
from src.graph.drag.DragCanvas import DragCanvas
from src.graph.helpers.ToolbarHelper import ToolbarHelper
from src.graph.helpers.CanvasHelper import CanvasHelper
from src.utils.Vector import Vector
from src.graph.elements.CanvasElement import CanvasElement
from src.state.GraphState import graph_state, GraphState
from src.graph.commands.Command import AddNodeCommand, DeleteElementCommand, CreateGraphCommand, CommandHistory, LoadGraphCommand, MoveElementCommand
import src.constance as const
from src.graph.GraphConfig import GraphConfig
from src.graph.helpers.GraphStrategy import GraphSelector
from src.GraphFile import GraphFile
from src.graph.AddEdgeManager import EdgePreviewManager
from typing import TYPE_CHECKING
from src.graph.CanvasGroup import CanvasGroup
from src.utils.Simulation import PathSimulation
if TYPE_CHECKING:
    from src.ui.GraphSheets import GraphSheets
    from src.ui.Menu.TabMenu import TabMenu
import uuid

class GraphController:
    def __init__(self, root, view: GraphCanvas, toolbar: ToolBar, file_manager: FileManager):
        self.current_graph: GraphState = GraphState(GraphModel())
        self.canvas_group = CanvasGroup(root, self)
        self.canvas_group.canvas_list.append(view)
        self.graphs: list[GraphModel] = [self.current_graph.get()]
        self.view = view
        self.view.pack(side='left', fill='both', expand=True)
        self.root = root
        self.toolbar = toolbar
        self.toolbar.controller = self
        self.toolbar.graph = self.current_graph.get()
        self.toolbar.change_tool(Tools.SELECT, self.toolbar.select_button)
        self.file_manager = file_manager
        self.draw_config = DrawGraphConfig()
        self.drag = DragCanvas(view, self.draw_config, self.current_graph.get())
        self.canvas_helper = CanvasHelper(view)
        self.toolbar_helper = ToolbarHelper(toolbar, self.current_graph.get(), view, self.draw_config)
        self.command_history: CommandHistory = CommandHistory(self)
        self.graph_selector = GraphSelector()
        self.useless_graph_file = GraphFile(filename="graph.txt")
        self.tab_menu: TabMenu | None = None
        self.graph_sheets: GraphSheets | None = None
        self.simulation: PathSimulation = PathSimulation(self.current_graph.get(), self.view)

        self.current_graph.subscribe(self.on_current_graph_change)
        self.current_graph.subscribe(self.on_graph_change)
        graph_state.subscribe(self.on_graph_change)

        self.toolbar.on_delete(self.delete)
        self.toolbar.on_undo(self.undo)
        self.toolbar.on_redo(self.redo)
        self.toolbar.on_load(self.load_graph)
        self.toolbar.on_save(self.save_graph)
        self.drag.on_element_move(self.on_move_element)
        self.toolbar.selected_tool.subscribe(self.on_tool_change)

        self.canvas_group.bind_canvas_events(view)

    def simulate(self):
        if self.simulation.is_running:
            self.simulation.stop()
            self.tab_menu.current_tab_component.destroy_simulate() # type: ignore
            return

        if self.simulation.is_running == False and self.tab_menu.current_tab == 'Graph':
            self.simulation.start()
            self.tab_menu.current_tab_component.simulate(self.simulation) # type: ignore

    def turn_off_compare_mode(self):
        self.graphs.clear()
        self.canvas_group.destroy_canvases()
        canvas = self.canvas_group.create_canvas(self.current_graph.get())
        self.canvas_group.on_current_canvas_change(canvas)
    
    def check_isomorphic(self):
        if len(self.graphs) >= 2:
            self.tab_menu.current_tab_component.set_isomorphic_var([self.graph_sheets.find_button_by_id(self.graphs[0].tab_id).cget('text'), self.graph_sheets.find_button_by_id(self.graphs[1].tab_id).cget('text')], self.graphs[0] == self.graphs[1])
    
    def compare_graphs(self, graphs_ids: list[uuid.UUID]):
        if len(graphs_ids) >= 2:
            self.graphs.clear()
            self.canvas_group.destroy_canvases()
            for id in graphs_ids:
                graph = self.graph_sheets.get_graph_by_id(id)
                if graph:
                    canvas = self.canvas_group.create_canvas(graph)
                    self.canvas_group.on_current_canvas_change(canvas)
                    graph.canvas_id = canvas.id
                    self.graphs.append(graph)

            self.check_isomorphic()
            
    def set_model(self, model: GraphModel):
        self.toolbar.deselect_all_tool()
        model.canvas_id = self.view.id
        self.view.tab_id = model.tab_id
        self.current_graph.set(model)

    def on_tool_change(self, tool: Tools):
        self.toolbar_helper.on_tool_change(tool)
        if tool == Tools.SELECT or tool == Tools.ADD_EDGE:
            self.drag.is_drag_node = False
        else:
            self.drag.is_drag_node = True

    def on_graph_change(self, graph_model: GraphModel):
        self.toolbar.change_undo_button_style(self.command_history.can_undo())
        self.toolbar.change_redo_button_style(self.command_history.can_redo())
        self.toolbar.change_compare_button_style(len(self.graph_sheets.graph_sheets) >= 2)
    
    def on_current_graph_change(self, graph_model: GraphModel):
        self.view.graph = graph_model
        self.toolbar.graph = graph_model
        self.toolbar_helper.graph = graph_model
        self.drag.graph = graph_model
        for i, sheet in enumerate(self.graph_sheets.graph_sheets):
            if sheet.canvas_id == self.view.graph.canvas_id and sheet.tab_id == self.view.graph.tab_id:
                self.graph_sheets.graph_sheets[i] = graph_model
                break
        self.simulation.set_model(graph_model)
        self.check_isomorphic()
        self.view.draw_graph()

    def path_search(self):
        path = self.view.search_path()

        if path:
            self.toolbar.change_simulate_button_style(True)
        else:
            self.toolbar.change_simulate_button_style(False)

    def on_move_element(self, element: CanvasElement, position: Vector, old_position: Vector):
        self.command_history.execute_command(MoveElementCommand(self, element, position, old_position))
        graph_state.set(self.current_graph.get())

    def load_graph(self, path: str):
        graph = self.file_manager.load(path)
        self.command_history.execute_command(LoadGraphCommand(self, graph))
        graph_state.set(self.current_graph.get())

    def save_graph(self, path: str):
        self.file_manager.save(self.current_graph.get(), path)

    def add_node(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_NODE and self.toolbar_helper.node_preview and const.MAX_NODE_COUNT > len(self.current_graph.get().nodes):
            self.command_history.execute_command(AddNodeCommand(self, self.toolbar_helper.node_preview))
            graph_state.set(self.current_graph.get())   

    def add_edge(self, event):
        EdgePreviewManager(self).add_edge(event)

    def select(self, event):
        if self.toolbar.get_selected_tool() == Tools.SELECT:
            element = self.canvas_helper.find_elemment_under_cursor(event, self.current_graph.get().get_graph_elements())
            if element:
                self.toolbar.select(element)
                graph_state.set(self.current_graph.get())
                self.view.draw_graph()

    def delete(self, elements: list[CanvasElement]):
        if len(elements) == 0:
            return
        self.command_history.execute_command(DeleteElementCommand(self, elements))
        
        for element in elements:
            element.delete(self.view)
        self.toolbar.deselect_all_tool()
        graph_state.set(self.current_graph.get())
        self.view.draw_graph()

    def undo(self):
        self.command_history.undo()
        graph_state.set(self.current_graph.get())
    
    def redo(self):
        self.command_history.redo()
        graph_state.set(self.current_graph.get())

    def on_click(self, event):
        self.canvas_group.change_current_canvas(event.widget.id, True)
        if self.toolbar.get_selected_tool() != Tools.SELECT and self.toolbar.get_selected_tool() != Tools.ADD_EDGE:
            self.drag.drag_node(event)
        self.drag.drag_canvas(event)
        self.add_node(event)
        self.add_edge(event)
        self.select(event) 

    def change_mode(self, mode: str):
        self.mode = mode

    def on_drag(self, event):
        self.drag.drag(event)
        
    def on_release(self, event):
        self.drag.end_drag(event)
        if self.current_graph.get().nodes:
            self.current_graph.get().wages = self.current_graph.get().generator.generate_wages(self.current_graph.get(), self.current_graph.get().nodes)
            self.current_graph.set(self.current_graph.get())
        graph_state.set(self.current_graph.get())

    def motion(self, event):
        self.canvas_group.change_current_canvas(event.widget.id)
        self.view.change_cursor(event)
        self.toolbar_helper.show_node_preview(event)
        self.toolbar_helper.show_edge_preview(event)

    def create(self, config: GraphConfig):
        self.view.is_intersection = config.is_show_intersections
        self.command_history.execute_command(CreateGraphCommand(self, config, self.graph_selector.get_graph_type(self.tab_menu.current_tab))) # type: ignore
        if self.graph_sheets is not None and len(self.graph_sheets) == 0:
            self.graph_sheets.add_graph_sheet(self.current_graph.get(), "New graph", True)
        self.useless_graph_file.save(self.current_graph.get(), "")
        graph_state.set(self.current_graph.get())

    def update(self, config: GraphConfig):
        self.view.is_intersection = config.is_show_intersections
        model = self.current_graph.get()
        model.config = config
        self.current_graph.set(model)
        self.useless_graph_file.save(self.current_graph.get(), "")
        graph_state.set(self.current_graph.get())
