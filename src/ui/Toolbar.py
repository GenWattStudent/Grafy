from __future__ import annotations
import customtkinter as ctk
from src.Theme import Theme
from src.state.State import State
from src.ui.SwitchButton import SwitchButton
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphModel import GraphModel
from enum import Enum
from src.utils.Event import Event
from src.state.GraphState import graph_state


class Tools(Enum):
    EMPTY = "EMPTY"
    SELECT = "SELECT"
    ADD_NODE = "ADD_NODE"
    ADD_EDGE = "ADD_EDGE"
    DELETE = "DELETE"

class ToolState(State):
    def __init__(self, initial_state: Tools = Tools.EMPTY):
        super().__init__(initial_state=initial_state)


class ToolBar(ctk.CTkFrame):
    def __init__(self, master: ctk.CTkFrame, root, graph: GraphModel, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.graph = graph
        self.root = root
        self.border_width = 2

        self.selected_tool: State = ToolState()
        self.prev_tool: State = ToolState()
        self.is_cleaned = False

        self.delete_event = Event()
        self.undo_event = Event()
        self.redo_event = Event()

        self.border = ctk.CTkLabel(self, text="", fg_color=Theme.get("text_color"))

        self.select_button = SwitchButton(self, text="Select")
        self.select_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.add_node_button = SwitchButton(self, text="Add Node")
        self.add_node_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.delete_button = SwitchButton(self, text="Delete", fg_color=Theme.get("error_color"), hover_color=Theme.get("error_hover_color"), state="disabled")
        self.delete_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.add_edge_button = SwitchButton(self, text="Add Edge")
        self.add_edge_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.undo_button = SwitchButton(self, text="Undo", state = "disabled")
        self.undo_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.redo_button = SwitchButton(self, text="Redo", state = "disabled")
        self.redo_button.pack(anchor="w", side="left", padx=10, pady=10)

        self.select_button.configure(command=lambda el=self.select_button: self.change_tool(Tools.SELECT, el))
        self.add_node_button.configure(command=lambda el=self.add_node_button: self.change_tool(Tools.ADD_NODE, el))
        self.delete_button.configure(command=self.delete_tool)
        self.undo_button.configure(command=self.undo)
        self.redo_button.configure(command=self.redo)
        self.add_edge_button.configure(command=lambda el=self.add_edge_button: self.change_tool(Tools.ADD_EDGE, el))

        self.bind("<Configure>", self.on_resize)
        self.root.bind("<Delete>", lambda event: self.delete_tool())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Escape>", lambda event: self.change_tool(Tools.EMPTY))

    def undo(self):
        self.undo_event()

    def redo(self):
        self.redo_event()

    def on_delete(self, cb):
        self.delete_event += cb

    def off_delete(self, cb):
        self.delete_event -= cb

    def on_undo(self, cb):
        self.undo_event += cb
    
    def off_undo(self, cb):
        self.undo_event -= cb

    def on_redo(self, cb):
        self.redo_event += cb
    
    def off_redo(self, cb):
        self.redo_event -= cb

    def change_delete_button_style(self, selected_elements: int):
        if selected_elements == 0:
            self.delete_button.configure(state = "disabled")
        else:
            self.delete_button.configure(state = "normal")

    def change_redo_button_style(self, can_redo: bool):
        if can_redo:
            self.redo_button.configure(state = "normal")
        else:
            self.redo_button.configure(state = "disabled")

    def change_undo_button_style(self, can_undo: bool):
        if can_undo:
            self.undo_button.configure(state = "normal")
        else:
            self.undo_button.configure(state = "disabled")

    def delete_tool(self):
        if len(self.graph.selected_elements) == 0:
            return

        # get node and edges to delete
        nodes_to_delete = self.graph.get_nodes_from_list(self.graph.selected_elements)
        edges_to_delete = self.graph.get_edges_from_list(self.graph.selected_elements)

        # add to delete also edges connected to nodes to delete
        for edge in self.graph.edges:
            if edge.node1 in nodes_to_delete or edge.node2 in nodes_to_delete:
                edges_to_delete.append(edge)


        self.graph.delete_edges(edges_to_delete)
        self.graph.delete_nodes(nodes_to_delete)
        self.delete_event(nodes_to_delete + edges_to_delete)
        self.change_tool(Tools.DELETE)

    def deselect_all(self):
        self.select_button.deselect()
        self.add_node_button.deselect()
        self.add_edge_button.deselect()

    def select(self, element):
        if element.is_selected:
            element.is_selected = False
            self.graph.selected_elements.remove(element)
            graph_state.set(self.graph)
            return
        element.is_selected = True
        self.graph.selected_elements.append(element)
        self.change_delete_button_style(len(self.graph.selected_elements))

    def deselect(self, element):
        element.is_selected = False
        self.graph.selected_elements.remove(element)
        self.change_delete_button_style(len(self.graph.selected_elements))

    def deselect_all_tool(self):
        for element in self.graph.selected_elements:
            element.is_selected = False
        self.graph.selected_elements.clear()
        self.change_delete_button_style(len(self.graph.selected_elements))

    def change_tool(self, tool: Tools, element: SwitchButton | None = None):
        self.deselect_all()
        if element is not None:
            element.toogle()
        self.is_cleaned = False
        if self.selected_tool.get() == tool and element is not None:
            self.prev_tool.set(self.selected_tool.get())
            self.selected_tool.set(Tools.EMPTY)
            element.deselect()
            return

        self.prev_tool.set(self.selected_tool.get())
        self.selected_tool.set(tool)

    def on_resize(self, event):
        self.border.configure(width=event.width)
        self.border.place(x=0, y=self.winfo_height() - self.border_width)

    def get_selected_tool(self) -> Tools:
        return self.selected_tool.get()

    def get_prev_tool(self) -> Tools:
        return self.prev_tool.get()
