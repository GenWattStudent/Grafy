import customtkinter as ctk
from src.Theme import Theme

class SwitchButton(ctk.CTkButton):
    def __init__(self, master, fg_color: str = Theme.get("canvas_bg_color"), hover_color: str = Theme.get("distinction_color"), **kw):
        super().__init__(master, **kw)
        self.master = master
        self.selected = False
        self.configure(
            fg_color = fg_color,
            hover_color = hover_color,
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

