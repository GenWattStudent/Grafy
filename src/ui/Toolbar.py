import customtkinter as ctk
from src.Theme import Theme
from enum import Enum


class Tools(Enum):
    EMPTY = "EMPTY"
    SELECT = "SELECT"
    ADD_NODE = "ADD_NODE"
    ADD_EDGE = "ADD_EDGE"


class SwitchButton(ctk.CTkButton):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.selected = False
        self.configure(
            fg_color=Theme.get("canvas_bg_color"),
            border_spacing=0, corner_radius=0)

    def select(self):
        self.selected = True
        self.configure(fg_color=Theme.get("secondary_color"))

    def deselect(self):
        self.selected = False
        self.configure(fg_color=Theme.get("canvas_bg_color"))

    def is_selected(self) -> bool:
        return self.selected

    def toogle(self):
        if self.selected:
            self.deselect()
        else:
            self.select()


class ToolBar(ctk.CTkFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.border_width = 2

        self.selected_tool: Tools = Tools.EMPTY
        self.prev_tool: Tools = Tools.EMPTY
        self.is_cleaned = False

        self.border = ctk.CTkLabel(self, text="", fg_color=Theme.get("text_color"))

        self.select_button = SwitchButton(self, text="Select")
        self.select_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.add_node_button = SwitchButton(self, text="Add Node")
        self.add_node_button.pack(anchor="w", side="left", padx=10, pady=10)
        self.add_edge_button = SwitchButton(self, text="Add Edge")
        self.add_edge_button.pack(anchor="w", side="left", padx=10, pady=10)

        self.select_button.configure(command=lambda el=self.select_button: self.change_tool(Tools.SELECT, el))
        self.add_node_button.configure(command=lambda el=self.add_node_button: self.change_tool(Tools.ADD_NODE, el))
        self.add_edge_button.configure(command=lambda el=self.add_edge_button: self.change_tool(Tools.ADD_EDGE, el))

        self.bind("<Configure>", self.on_resize)

    def deselect_all(self):
        self.select_button.deselect()
        self.add_node_button.deselect()
        self.add_edge_button.deselect()

    def change_tool(self, tool: Tools, element: SwitchButton):
        self.deselect_all()
        element.toogle()
        self.is_cleaned = False
        if self.selected_tool == tool:
            self.prev_tool = self.selected_tool
            self.selected_tool = Tools.EMPTY
            element.deselect()
            return

        self.prev_tool = self.selected_tool
        self.selected_tool = tool

    def on_resize(self, event):
        self.border.configure(width=event.width)
        self.border.place(x=0, y=self.winfo_height() - self.border_width)

    def get_selected_tool(self) -> Tools:
        return self.selected_tool

    def get_prev_tool(self) -> Tools:
        return self.prev_tool
