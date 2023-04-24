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
from copy import copy


class Command(ABC):
    def __init__(self, controller: GraphController):
        self.controller = controller

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def redo(self):
        pass

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
        self.controller = controller
        self.node = node

    def execute(self):
        self.controller.current_graph.get().add_node(self.node)

    def undo(self):
        self.controller.current_graph.get().delete_node(self.node)
        self.controller.view.draw_graph()

    def redo(self):
        self.execute()
        self.controller.view.draw_graph()

class AddEdgeCommand(Command):
    def __init__(self, controller: GraphController, edge: Edge):
        self.controller = controller
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
        self.controller = controller
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
        self.graph_model = graph_model
        self.config = config
        self.controller = controller

    def execute(self):
        self.controller.toolbar.deselect_all_tool()
        self.graph_model.update(self.controller.view, self.config)
        self.graph_model.create(self.controller.view)
        self.controller.current_graph.set(self.graph_model)

    def undo(self):
        self.controller.toolbar.deselect_all_tool()
        #loop through the undo stack and find the last CreateGraphCommand
        for i in range(len(self.controller.command_history.undo_stack) - 1, -1, -1):
            if isinstance(self.controller.command_history.undo_stack[i], CreateGraphCommand):
                prev_graph_model = self.controller.command_history.undo_stack[i].graph_model
                self.controller.current_graph.set(prev_graph_model)
                self.controller.view.draw_graph()
                break

    def redo(self):
        self.controller.toolbar.deselect_all_tool()
        self.controller.current_graph.set(self.graph_model)
        self.controller.view.draw_graph()

class LoadGraphCommand(Command): 
    def __init__(self, controller: GraphController, graph_model: GraphModel):
        self.graph_model = graph_model
        self.controller = controller

    def execute(self):
        self.controller.toolbar.deselect_all_tool()
        self.controller.current_graph.set(self.graph_model)
        self.controller.view.draw_graph()
    
    def undo(self):
        self.controller.toolbar.deselect_all_tool()
        #loop through the undo stack and find the last LoadGraphCommand
        for i in range(len(self.controller.command_history.undo_stack) - 1, -1, -1):
            if isinstance(self.controller.command_history.undo_stack[i], LoadGraphCommand) or isinstance(self.controller.command_history.undo_stack[i], CreateGraphCommand):
                prev_graph_model = self.controller.command_history.undo_stack[i].graph_model
                self.controller.current_graph.set(prev_graph_model)
                self.controller.view.draw_graph()
                break

    def redo(self):
        self.execute()