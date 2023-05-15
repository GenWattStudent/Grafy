from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController
from src.state.GraphState import graph_state
from src.graph.commands.Command import AddEdgeCommand
from src.graph.elements.Edge import Edge
from src.graph.elements.Node import Node
from src.ui.Toolbar import Tools
from src.utils.Vector import Vector

class EdgePreviewManager:
    def __init__(self, controller: GraphController):
        self.controller = controller

    def add_edge(self, event):
        if self.controller.toolbar.get_selected_tool() == Tools.ADD_EDGE:
            x, y = self.controller.canvas_helper.canvas_to_graph_coords(event.x, event.y)
            for node in self.controller.current_graph.get().nodes:
                if node.is_under_cursor(Vector(x, y)):
                    if len(self.controller.current_graph.get().selected_elements) == 0:
                        self.controller.toolbar.select(node)
                    else:
                        node2 = self.controller.current_graph.get().selected_elements[0]
                        if isinstance(node2, Node) and node != node2:
                            # if edge already exists, do nothing
                            if self.edge_exists(node, node2):
                                return
                            self.execute_add_edge_command(node, node2)
                            break

        graph_state.set(self.controller.current_graph.get())
        self.controller.view.draw_graph()

    def edge_exists(self, node1, node2):
        for edge in self.controller.current_graph.get().edges:
            if (edge.node1 == node2 and edge.node2 == node1) or (edge.node1 == node1 and edge.node2 == node2):
                return True
        return False

    def execute_add_edge_command(self, node1, node2):
        self.controller.command_history.execute_command(AddEdgeCommand(self.controller, Edge(node1, node2)))
        self.controller.toolbar.deselect(node2)
        self.controller.toolbar.select(node1)
        self.controller.view.draw_nodes_and_edges()
