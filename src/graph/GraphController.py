from src.graph.GraphModel import GraphModel
from src.ui.GraphCanvas import GraphCanvas
from src.GraphFile import GraphFile
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.ui.Toolbar import ToolBar, Tools
from src.graph.drag.DragCanvas import DragCanvas
from src.graph.helpers.ToolbarHelper import ToolbarHelper
from src.graph.helpers.CanvasHelper import CanvasHelper
from src.utils.Vector import Vector
from src.graph.elements.Edge import Edge
from src.graph.elements.Node import Node
from src.graph.elements.CanvasElement import CanvasElement
from src.state.GraphState import graph_state, GraphState
from src.graph.commands.Command import AddNodeCommand, AddEdgeCommand, DeleteElementCommand, CreateGraphCommand, CommandHistory
import src.constance as const
from src.graph.GraphConfig import GraphConfig


class GraphController:
    def __init__(self, view: GraphCanvas, toolbar: ToolBar, file_manager: GraphFile, current_mode: str):
        self.current_graph: GraphState = GraphState(GraphModel())
        self.view = view
        self.toolbar = toolbar
        self.file_manager = file_manager
        self.draw_config = DrawGraphConfig()
        self.drag = DragCanvas(view, self.draw_config, self.current_graph.get())
        self.canvas_helper = CanvasHelper(view)
        self.toolbar_helper = ToolbarHelper(toolbar, self.current_graph.get(), view, self.draw_config)
        self.command_history: CommandHistory = CommandHistory()
        self.mode = current_mode

        self.current_graph.subscribe(self.on_current_graph_change)
        graph_state.subscribe(self.on_graph_change)

        self.toolbar.on_delete(self.delete)
        self.toolbar.on_undo(self.undo)
        self.toolbar.on_redo(self.redo)
        self.toolbar.selected_tool.subscribe(self.on_tool_change)

        self.view.bind("<Button-1>", self.on_click)
        self.view.bind("<B1-Motion>", self.on_drag)
        self.view.bind("<Motion>", self.motion)
        self.view.bind("<ButtonRelease-1>", self.on_release)

    def on_tool_change(self, tool: Tools):
        self.toolbar_helper.on_tool_change(tool)
        if tool == Tools.SELECT or tool == Tools.ADD_EDGE:
            self.drag.is_drag_node = False
        else:
            self.drag.is_drag_node = True

    def on_graph_change(self, graph_model: GraphModel):
        self.toolbar.change_undo_button_style(self.command_history.can_undo())
        self.toolbar.change_redo_button_style(self.command_history.can_redo())
    
    def on_current_graph_change(self, graph_model: GraphModel):
        self.view.graph = graph_model
        self.toolbar.graph = graph_model
        self.toolbar_helper.graph = graph_model
        self.drag.graph = graph_model
        self.view.draw_graph()

    def add_node(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_NODE and self.toolbar_helper.node_preview and const.MAX_NODE_COUNT > len(self.current_graph.get().nodes):
            self.command_history.execute_command(AddNodeCommand(self, self.toolbar_helper.node_preview))
            self.toolbar_helper.node_preview.delete(self.view)
            self.toolbar_helper.node_preview = None
            graph_state.set(self.current_graph.get())   
            self.view.draw_graph()

    def add_edge(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            for node in self.current_graph.get().nodes:
                if node.is_under_cursor(Vector(x, y)):
                    if len(self.current_graph.get().selected_elements) == 0:
                        self.toolbar.select(node)
                    else:
                        node2 = self.current_graph.get().selected_elements[0]
                        if isinstance(node2, Node) and node != node2:
                            # if edge already exists, do nothing
                            if any(edge for edge in self.current_graph.get().edges if (edge.node1 == node2 and edge.node2 == node) or (edge.node1 == node and edge.node2 == node2)):
                                return
                            self.command_history.execute_command(AddEdgeCommand(self, Edge(node2, node)))
                            self.toolbar.deselect(node2)
                            self.toolbar.select(node)
                            self.view.draw_nodes_and_edges()
                            break
            graph_state.set(self.current_graph.get())            
            self.view.draw_graph()

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
        self.drag.click(event)
        self.add_node(event)
        self.add_edge(event)
        self.select(event) 

    def change_mode(self, mode: str):
        self.mode = mode

    def on_drag(self, event):
        self.drag.drag(event)

    def on_release(self, event):
       self.drag.end_drag(event)
       self.current_graph.get().wages = self.current_graph.get().generator.generate_wages(self.current_graph.get(), self.current_graph.get().nodes)
       self.current_graph.set(self.current_graph.get())
       graph_state.set(self.current_graph.get())

    def motion(self, event):
        self.view.change_cursor(event)
        self.toolbar_helper.show_node_preview(event)
        self.toolbar_helper.show_edge_preview(event)

    def create(self, config: GraphConfig):
        if self.mode == "Graph":
            self.command_history.execute_command(CreateGraphCommand(self, config))
        elif self.mode == "Tree":
            # self.current_graph.get().tree.update(self.view, config)
            self.current_graph.get().create(self.view)
        self.view.is_intersection = config.is_show_intersections
        self.file_manager.save(self.current_graph.get())
        graph_state.set(self.current_graph.get())

    def update(self, config: GraphConfig):
        self.toolbar.deselect_all_tool()
        self.view.is_intersection = config.is_show_intersections
        self.current_graph.get().update(self.view, config)
        self.view.draw_graph()
        self.file_manager.save(self.current_graph.get())
        graph_state.set(self.current_graph.get())
