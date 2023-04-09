from src.graph.Graph import Graph
from src.ui.GraphCanvas import GraphCanvas
from src.GraphFile import GraphFile
from src.graph.DrawGraphConfig import DrawGraphConfig
from src.ui.Toolbar import ToolBar, Tools
from src.graph.drag.dragCanvas import DragCanvas
from src.utils.Vector import Vector
from src.graph.elements.Edge import Edge
from src.state.GraphState import graph_state
import src.constance as const


class GraphController:
    def __init__(self, model: Graph, view: GraphCanvas, toolbar: ToolBar, file_manager: GraphFile):
        self.model = model
        self.view = view
        self.toolbar = toolbar
        self.file_manager = file_manager
        self.draw_config = DrawGraphConfig()
        self.canvas_helper = DragCanvas(view, self.draw_config, model)

        self.toolbar.on_delete(self.delete)
        self.toolbar.selected_tool.subscribe(self.canvas_helper.on_tool_change)

        self.view.bind("<Button-1>", self.on_click)
        self.view.bind("<B1-Motion>", self.on_drag)
        self.view.bind("<Motion>", self.motion)
        self.view.bind("<ButtonRelease-1>", self.on_release)

    def add_node(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_NODE and self.canvas_helper.node_preview and const.MAX_NODE_COUNT > len(self.model.nodes):
            self.model.add_node(self.canvas_helper.node_preview)
            graph_state.set(self.model)
            self.canvas_helper.node_preview.delete(self.view)
            self.canvas_helper.node_preview = None
            self.view.draw_graph()

    def add_edge(self, event):
        if self.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            if self.model.is_toolbar() and self.model.toolbar.get_selected_tool() == Tools.ADD_EDGE:
                for node in self.model.nodes:
                    if node.is_under_cursor(Vector(x, y)):
                        if len(self.model.toolbar.selected_elements) == 0:
                            self.model.toolbar.select_tool(node)
                        else:
                            self.model.add_edge(Edge(self.model.toolbar.selected_elements[0], node))
                            self.model.toolbar.deselect_all_tool()
                            self.view.draw_nodes_and_edges()
                            break
            self.view.draw_graph()
            graph_state.set(self.model)

    def select(self, event):
        if self.toolbar.get_selected_tool() == Tools.SELECT:
            element = self.canvas_helper.find_elemment_under_cursor(event)
            if element:
                self.model.select(element)
                self.view.draw_graph()
                graph_state.set(self.model)

    def delete(self, elements: list):
        for element in elements:
            element.delete(self.view)
        self.model.delete_selected()
        graph_state.set(self.model)
        self.view.draw_graph()

    def drag_canvas(self, event):
        if not self.canvas_helper.draging_node:
            self.view.scan_mark(event.x, event.y)

    def end_drag(self, event):
        if self.canvas_helper.draging_node:
            self.canvas_helper.draging_node.is_dragged = False
            self.canvas_helper.draging_node.radius = self.draw_config.node_radius

            self.model.generator.set_dragged_edges(self.model.edges, self.canvas_helper.draging_node, False)
            self.draging_node = None
            self.view.draw_graph()
            graph_state.set(self.model)
            return

        self.view.scan_dragto(event.x, event.y, gain=1)

    def start_drag_node(self, event):
        x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
        for node in self.model.nodes:
            if node.is_under_cursor(Vector(x, y)):
                self.canvas_helper.draging_node = node
                self.canvas_helper.draging_node.radius = self.draw_config.dragged_node_radius
                self.model.generator.set_dragged_edges(self.model.edges, node)

    def on_click(self, event):
        self.add_node(event)
        self.add_edge(event)
        self.select(event)
        self.start_drag_node(event)
        self.drag_canvas(event)

    def drag_node(self, event):
        if self.canvas_helper.draging_node:
            x, y = self.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            self.canvas_helper.draging_node.position.x = x
            self.canvas_helper.draging_node.position.y = y
            self.canvas_helper.draging_node.is_dragged = True
            self.view.delete("all")
            self.view.draw_edges(self.model.edges)
            self.view.draw_nodes(self.model.nodes)
            return

        self.view.scan_dragto(event.x, event.y, gain=1)

    def on_drag(self, event):
        self.drag_node(event)

    def on_release(self, event):
        self.end_drag(event)

    def motion(self, event):
        self.view.change_cursor(event)
        if self.toolbar.get_selected_tool() == Tools.ADD_NODE:
            self.canvas_helper.show_node_preview(event)
