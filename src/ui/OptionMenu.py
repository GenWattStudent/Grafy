import ttkbootstrap as ttk
from typing import Callable

class OptionMenuValue:
    def __init__(self, label: str, callback: Callable):
        self.label = label
        self.callback = callback

class OptionMenu(ttk.Menu):
    def __init__(self, parent, schema: list[OptionMenuValue], *args):
        super().__init__(parent, *args)
        self.schema = schema

        for value in schema:
            self.add_command(label=value.label, command=value.callback)

    def show(self, event):
        self.post(event.x_root, event.y_root)