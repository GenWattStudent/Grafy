from __future__ import annotations
from abc import ABC, abstractmethod
from src.graph.GraphModel import Graph, GraphModel
from src.graph.elements.Node import Node
from src.graph.elements.Edge import Edge
from src.graph.elements.CanvasElement import CanvasElement
from src.graph.GraphConfig import GraphConfig
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController
from src.utils.Vector import Vector
from copy import copy


class Command(ABC):
    def __init__(self, controller: GraphController):
        self.controller = controller
        self.graph_model: GraphModel = copy(controller.current_graph.get())

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    def redo(self):
        self.execute()

class CommandHistory:
    def __init__(self):
        self.undo_stack: list[Command] = []
        self.redo_stack: list[Command] = []

    def get_undo_command_by_index(self, index: int) -> Command:
        return self.undo_stack[index]

    def can_undo(self) -> bool:
        return len(self.undo_stack) > 1
    
    def can_redo(self) -> bool:
        return len(self.redo_stack) > 0

    def execute_command(self, command: Command):
        command.execute()
        self.undo_stack.append(command)
        self.redo_stack.clear()

    def undo(self):
        if len(self.undo_stack) > 1:
            command = self.undo_stack.pop()
            command.undo()
            self.redo_stack.append(command)

    def redo(self):
        if self.redo_stack:
            command = self.redo_stack.pop()
            command.redo()
            self.undo_stack.append(command)

class AddNodeCommand(Command):
    def __init__(self, controller: GraphController, node: Node):
        super().__init__(controller)
        self.node = node

    def execute(self):
        if self.controller.toolbar_helper.node_preview is not None:
            self.controller.toolbar_helper.node_preview.delete(self.controller.view)
            self.controller.toolbar_helper.node_preview = None
        self.controller.current_graph.get().add_node(self.node)
        self.controller.view.draw_graph()

    def undo(self):
        self.controller.current_graph.get().delete_node(self.node)
        self.controller.view.draw_graph()

    def redo(self):
        self.execute()
        self.controller.view.draw_graph()

class AddEdgeCommand(Command):
    def __init__(self, controller: GraphController, edge: Edge):
        super().__init__(controller)
        self.edge = edge

    def execute(self):
        self.controller.current_graph.get().add_edge(self.edge)

    def undo(self):
        self.controller.current_graph.get().delete_edge(self.edge)
        self.controller.view.draw_graph()

    def redo(self):
        self.execute()
        self.controller.view.draw_graph()


class DeleteElementCommand(Command):
    def __init__(self, controller: GraphController, elements: list[CanvasElement]):
        super().__init__(controller)
        self.elements = copy(elements)

    def execute(self):
        for element in self.elements:
            self.controller.current_graph.get().delete_element(element)

    def undo(self):
        for element in self.elements:
            self.controller.current_graph.get().add_element(element)
        
        self.controller.view.draw_graph()
    
    def redo(self):
        self.execute()
        self.controller.view.draw_graph()

class CreateGraphCommand(Command):
    def __init__(self, controller: GraphController, config: GraphConfig, graph_model: GraphModel = Graph()):
        super().__init__(controller)
        self.graph_model = graph_model
        self.config = config

    def execute(self):
        self.controller.toolbar.deselect_all_tool()
        self.graph_model.create(self.controller.view, self.config)
        self.controller.current_graph.set(self.graph_model)

    def undo(self):
        self.controller.toolbar.deselect_all_tool()
        commandHistory = self.controller.command_history
        prev_graph_model = commandHistory.undo_stack[len(commandHistory.undo_stack) - 1].graph_model
        self.controller.current_graph.set(prev_graph_model)
        self.controller.view.draw_graph()     

    def redo(self):
        self.controller.toolbar.deselect_all_tool()
        self.controller.current_graph.set(self.graph_model)
        self.controller.view.draw_graph()

class LoadGraphCommand(Command): 
    def __init__(self, controller: GraphController, graph_model: GraphModel):
        super().__init__(controller)
        self.graph_model = graph_model

    def execute(self):
        self.controller.toolbar.deselect_all_tool()
        self.controller.current_graph.set(self.graph_model)
        self.controller.view.draw_graph()
    
    def undo(self):
        self.controller.toolbar.deselect_all_tool()
        commandHistory = self.controller.command_history
        prev_graph_model = commandHistory.undo_stack[len(commandHistory.undo_stack) - 1].graph_model
        self.controller.current_graph.set(prev_graph_model)
        self.controller.view.draw_graph()

class UpdateGraphCommand(Command):
    def __init__(self, controller: GraphController, config: GraphConfig):
        super().__init__(controller)
        self.config = config
    
    def execute(self):
        self.controller.toolbar.deselect_all_tool()
        self.controller.view.is_intersection = self.config.is_show_intersections
        self.controller.current_graph.set(self.graph_model)
        self.controller.current_graph.get().update(self.controller.view, self.config)
        self.controller.view.draw_graph()
    
    def undo(self):
        self.controller.toolbar.deselect_all_tool()
        commandHistory = self.controller.command_history
        prev_graph_model = commandHistory.undo_stack[len(commandHistory.undo_stack) - 1].graph_model
        self.controller.current_graph.set(prev_graph_model)
        self.controller.view.draw_graph()

class MoveElementCommand(Command):
    def __init__(self, controller: GraphController, element: CanvasElement, new_position: Vector, old_position: Vector):
        super().__init__(controller)
        self.element = element
        self.new_position = new_position
        self.old_position = old_position

    def execute(self):
        self.element.position = self.new_position
        self.controller.view.draw_graph()

    def undo(self):
        self.element.position = self.old_position
        self.controller.view.draw_graph()