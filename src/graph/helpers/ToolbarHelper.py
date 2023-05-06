from src.graph.helpers.CanvasHelper import CanvasHelper
from src.graph.GraphModel import GraphModel
from src.graph.elements.Node import Node
from src.ui.GraphCanvas import GraphCanvas
from src.ui.Toolbar import ToolBar, Tools
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.utils.Vector import Vector

class ToolbarHelper:
    def __init__(self, toolbar: ToolBar, graph: GraphModel, canvas: GraphCanvas, draw_config: DrawGraphConfig):
        self.toolbar = toolbar
        self.graph = graph
        self.canvas = canvas
        self.draw_config = draw_config
        self.canvas_helper = CanvasHelper(canvas)
        self.node_preview = None
        self.edge_preview = None

        self.toolbar.selected_tool.subscribe(self.on_tool_change)

    def on_tool_change(self, tool: Tools):
        if self.toolbar.get_prev_tool() == Tools.SELECT:
            self.toolbar.deselect_all_tool()
            self.canvas.draw_nodes_and_edges()
        elif self.toolbar.get_prev_tool() == Tools.ADD_EDGE:
            self.toolbar.deselect_all_tool()
            if self.edge_preview:
                self.canvas.delete(self.edge_preview)
                self.edge_preview = None
            self.canvas.draw_nodes(self.graph.nodes)
        elif self.toolbar.get_prev_tool() == Tools.ADD_NODE and self.node_preview:
            self.node_preview.delete(self.canvas)
            self.node_preview = None
        if self.toolbar.get_selected_tool() == Tools.DELETE:
            self.canvas.draw_graph()

    def show_node_preview(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_NODE:
            if self.node_preview:
                self.node_preview.delete(self.canvas)
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            pos = Vector(x, y)
            index = 1
            if len(self.graph.nodes) > 0:
                index = len(self.graph.nodes) + 1
            self.node_preview = Node(pos, index, self.draw_config.node_radius)
            self.node_preview.draw(self.canvas)
    
    def show_edge_preview(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            selected_nodes = self.graph.get_nodes_from_list(self.graph.selected_elements)

            if len(selected_nodes) == 1:
                self.edge_preview = self.canvas.draw_edge_preview(event, selected_nodes[0])

    def select(self, event):
        x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
        if self.toolbar.get_selected_tool() == Tools.SELECT:
            for element in self.graph.get_graph_elements():
                if element.is_under_cursor(Vector(x, y)):
                    self.toolbar.select(element)
                    self.canvas.draw_nodes_and_edges()
                    break
