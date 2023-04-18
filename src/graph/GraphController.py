from src.graph.GraphModel import GraphModel
from src.ui.GraphCanvas import GraphCanvas
from src.GraphFile import GraphFile
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.ui.Toolbar import ToolBar, Tools
from src.graph.drag.dragCanvas import DragCanvas
from src.graph.helpers.ToolbarHelper import ToolbarHelper
from src.graph.helpers.CanvasHelper import CanvasHelper
from src.utils.Vector import Vector
from src.graph.elements.Edge import Edge
from src.graph.elements.Node import Node
from src.state.GraphState import graph_state
from src.graph.commands.Command import AddNodeCommand, Command, AddEdgeCommand, DeleteElementCommand
import src.constance as const
from src.graph.GraphConfig import GraphConfig


class GraphController:
    def __init__(self, model: GraphModel, view: GraphCanvas, toolbar: ToolBar, file_manager: GraphFile, current_mode: str):
        self.model = model
        self.view = view
        self.toolbar = toolbar
        self.file_manager = file_manager
        self.draw_config = DrawGraphConfig()
        self.drag = DragCanvas(view, self.draw_config, model)
        self.canvas_helper = CanvasHelper(view)
        self.toolbar_helper = ToolbarHelper(toolbar, model, view, self.draw_config)
        self.history: list[Command] = []
        self.mode = current_mode

        self.toolbar.on_delete(self.delete)
        self.toolbar.on_undo(self.undo)
        self.toolbar.selected_tool.subscribe(self.toolbar_helper.on_tool_change)

        self.view.bind("<Button-1>", self.on_click)
        self.view.bind("<B1-Motion>", self.on_drag)
        self.view.bind("<Motion>", self.motion)
        self.view.bind("<ButtonRelease-1>", self.on_release)

    def add_node(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_NODE and self.toolbar_helper.node_preview and const.MAX_NODE_COUNT > len(self.model.nodes):
            add_node_command = AddNodeCommand(self.model, self.toolbar_helper.node_preview)
            add_node_command.execute()
            self.history.append(add_node_command)
            self.toolbar_helper.node_preview.delete(self.view)
            self.toolbar_helper.node_preview = None
            graph_state.set(self.model)   
            self.view.draw_graph()

    def add_edge(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            for node in self.model.nodes:
                if node.is_under_cursor(Vector(x, y)):
                    if len(self.model.selected_elements) == 0:
                        self.toolbar.select(node)
                    else:
                        node2 = self.model.selected_elements[0]
                        if isinstance(node2, Node) and node != node2:
                            # if edge already exists, do nothing
                            if any(edge for edge in self.model.edges if (edge.node1 == node2 and edge.node2 == node) or (edge.node1 == node and edge.node2 == node2)):
                                return
                            add_edge_command = AddEdgeCommand(self.model, Edge(node2, node))
                            add_edge_command.execute()
                            self.history.append(add_edge_command)
                            self.toolbar.deselect(node2)
                            self.toolbar.select(node)
                            self.view.draw_nodes_and_edges()
                            break
            graph_state.set(self.model)            
            self.view.draw_graph()

    def select(self, event):
        if self.toolbar.get_selected_tool() == Tools.SELECT:
            element = self.canvas_helper.find_elemment_under_cursor(event, self.model.get_graph_elements())
            if element:
                self.toolbar.select(element)
                self.view.draw_graph()
                graph_state.set(self.model)

    def delete(self, elements: list):
        if len(elements) == 0:
            return
        delete_command = DeleteElementCommand(self.model, elements)
        delete_command.execute()
        self.history.append(delete_command)
        
        for element in elements:
            element.delete(self.view)
        self.toolbar.deselect_all_tool()
        graph_state.set(self.model)
        self.view.draw_graph()

    def undo(self):
        if len(self.history) > 0:
            self.history.pop().undo()
            graph_state.set(self.model)
            self.view.draw_graph()

    def on_click(self, event):
        self.toolbar.focus_set()
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

    def motion(self, event):
        self.view.change_cursor(event)
        self.toolbar_helper.show_node_preview(event)
        self.toolbar_helper.show_edge_preview(event)

    def create(self, config: GraphConfig):
        if self.mode == "Graph":
            self.model.graph.update(self.view, config)
            self.model.graph.create(self.view)
        elif self.mode == "Tree":
            # self.model.tree.update(self.view, config)
            self.model.tree.create(self.view)
        self.view.is_intersection = config.is_show_intersections
        self.view.draw_graph()
        graph_state.set(self.model)

    def update(self, config: GraphConfig):
        self.view.is_intersection = config.is_show_intersections
        self.model.update(config, self.view)
        self.view.draw_graph()
        graph_state.set(self.model)
