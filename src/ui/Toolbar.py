from __future__ import annotations
import ttkbootstrap as ttk
from src.state.State import State
from src.ui.SwitchButton import SwitchButton
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController
    from src.graph.GraphModel import GraphModel
from enum import Enum
from src.utils.Event import Event
from src.state.GraphState import graph_state
from tkinter import filedialog
from ttkbootstrap.tooltip import ToolTip
from src.ui.windows.ChooseGraph import ChooseGraph
from src.ui.windows.Raport import Raport
import uuid

class Tools(Enum):
    EMPTY = "EMPTY"
    SELECT = "SELECT"
    ADD_NODE = "ADD_NODE"
    ADD_EDGE = "ADD_EDGE"
    DELETE = "DELETE"

class ToolState(State):
    def __init__(self, initial_state: Tools = Tools.EMPTY):
        super().__init__(initial_state=initial_state)


class ToolBar(ttk.Frame):
    def __init__(self, master: ttk.Frame, root, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.controller: GraphController | None = None
        self.graph: GraphModel | None = None
        self.root = root
        self.border_width = 2
        self.compare_select_window: ChooseGraph | None = None
        self.raport_window: Raport | None = None

        self.selected_tool: State = ToolState()
        self.prev_tool: State = ToolState()
        self.is_cleaned = False

        self.delete_event = Event()
        self.undo_event = Event()
        self.redo_event = Event()
        self.load_event = Event()
        self.save_event = Event()

        self.border = ttk.Label(self, text="", style="PRIMARY.TButton")

        self.select_button = SwitchButton(self, text="Select")
        self.select_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.add_node_button = SwitchButton(self, text="Add Node")
        self.add_node_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.add_edge_button = SwitchButton(self, text="Add Edge")
        self.add_edge_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.delete_button = SwitchButton(self, text="Delete", danger=True, state="disabled")
        self.delete_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.undo_button = SwitchButton(self, text="Undo", state = "disabled")
        self.undo_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.redo_button = SwitchButton(self, text="Redo", state = "disabled")
        self.redo_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.save_button = SwitchButton(self, text="Save")
        self.save_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.load_button = SwitchButton(self, text="Load")
        self.load_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.compare_button = SwitchButton(self, text="Compare")
        self.compare_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.raport_button = SwitchButton(self, text="Raport")
        self.raport_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.simulate_button = SwitchButton(self, text="Simulate", state="disabled")
        self.simulate_button.pack(anchor="w", side="left", padx=10, pady=10)

        self.select_tooltip = ToolTip(self.select_button, text="Select\nShortcut: s", bootstyle="info")
        self.add_node_tooltip = ToolTip(self.add_node_button, text="Add Node\nShortcut: n", bootstyle="info")
        self.add_edge_tooltip = ToolTip(self.add_edge_button, text="Add Edge\nShortcut: e", bootstyle="info")
        self.delete_tooltip = ToolTip(self.delete_button, text="Delete\nShortcut: Delete", bootstyle="info")
        self.undo_tooltip = ToolTip(self.undo_button, text="Undo\nShortcut: Ctrl + z", bootstyle="info")
        self.redo_tooltip = ToolTip(self.redo_button, text="Redo\nShortcut: Ctrl + y", bootstyle="info")
        self.save_tooltip = ToolTip(self.save_button, text="Save\nShortcut: Ctrl + s", bootstyle="info")
        self.load_tooltip = ToolTip(self.load_button, text="Load\nShortcut: Ctrl + o", bootstyle="info")
        self.compare_tooltip = ToolTip(self.compare_button, text="Compare", bootstyle="info")
        self.raport_tooltip = ToolTip(self.raport_button, text="Raport PDF", bootstyle="info")
        self.simulate_tooltip = ToolTip(self.simulate_button, text="Simulate", bootstyle="info")

        self.select_button.configure(command=lambda el=self.select_button: self.change_tool(Tools.SELECT, el))
        self.add_node_button.configure(command=lambda el=self.add_node_button: self.change_tool(Tools.ADD_NODE, el))
        self.delete_button.configure(command=self.delete_tool)
        self.undo_button.configure(command=self.undo)
        self.redo_button.configure(command=self.redo)
        self.add_edge_button.configure(command=lambda el=self.add_edge_button: self.change_tool(Tools.ADD_EDGE, el))
        self.load_button.configure(command=self.load)
        self.save_button.configure(command=self.save)
        self.compare_button.configure(command=self.compare)
        self.raport_button.configure(command=self.raport)
        self.simulate_button.configure(command=self.simulate)

        self.bind("<Configure>", self.on_resize)
        self.root.bind("<Delete>", lambda event: self.delete_tool())
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Escape>", lambda event: self.change_tool(Tools.EMPTY))
        self.root.bind("<Control-s>", lambda event: self.save())
        self.root.bind("<Control-o>", lambda event: self.load())
        self.root.bind("s", lambda event: self.change_tool(Tools.SELECT, self.select_button))
        self.root.bind("n", lambda event: self.change_tool(Tools.ADD_NODE, self.add_node_button))
        self.root.bind("e", lambda event: self.change_tool(Tools.ADD_EDGE, self.add_edge_button))
        self.root.bind('c', lambda event: self.compare())
        self.root.bind('r', lambda event: self.raport())
        self.root.bind('m', lambda event: self.simulate())

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

    def on_load(self, cb):
        self.load_event += cb
    
    def off_load(self, cb):
        self.load_event -= cb

    def on_save(self, cb):
        self.save_event += cb
    
    def off_save(self, cb):
        self.save_event -= cb
    
    def simulate(self):
        self.controller.simulate()

    def destroy_raport(self):
        if self.raport_window is not None:
            if self.raport_window.winfo_exists():
                self.raport_window.destroy()
            self.raport_window = None
    
    def raport(self):
        if self.raport_window is None:
            self.raport_window = Raport(self.root, "Raport", self.controller)
            self.raport_window.on_destroy(self.destroy_raport)
            self.raport_window.protocol("WM_DELETE_WINDOW", self.destroy_raport)
            self.raport_window.mainloop()
        else:
            self.destroy_raport()

    def load(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.load_event(file_path)

    def save(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.save_event(file_path)

    def change_simulate_button_style(self, can_simulate: bool):
        if can_simulate:
            self.simulate_button.configure(state = "normal")
        else:
            self.simulate_button.configure(state = "disabled")

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
    
    def change_compare_button_style(self, can_compare: bool):
        if can_compare:
            self.compare_button.configure(state = "normal")
        else:
            self.compare_button.configure(state = "disabled")

    def turn_off_compare_mode(self):
        self.compare_button.configure(state = "normal", text="Compare", command=self.compare)
        self.controller.turn_off_compare_mode()
    
    def change_to_turn_off_compare_mode(self, result: uuid.UUID):
        self.compare_select_window = None
        self.compare_button.configure(state = "normal", text="Turn off compare", command=self.turn_off_compare_mode)
        self.controller.compare_graphs(result)
    
    def destroy_compare_window(self):
        if self.compare_select_window is not None:
            if self.compare_select_window.winfo_exists():
                self.compare_select_window.destroy()
            self.compare_select_window = None
    
    def compare(self):
        if self.compare_select_window is None:
            self.compare_select_window = ChooseGraph(self.root, "Choose graph to compare", self.controller.graph_sheets)
            self.compare_select_window.on_close(self.change_to_turn_off_compare_mode)
            self.compare_select_window.protocol("WM_DELETE_WINDOW", self.destroy_compare_window)
            self.compare_select_window.mainloop()
        else:
            self.destroy_compare_window()

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
        self.border.place(x=0, rely=1, relwidth=1, height=self.border_width, y=-2)

    def get_selected_tool(self) -> Tools:
        return self.selected_tool.get()

    def get_prev_tool(self) -> Tools:
        return self.prev_tool.get()
