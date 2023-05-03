import ttkbootstrap as ttk

class SwitchButton(ttk.Button):
    def __init__(self, master, danger: bool = False, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.selected = False
        self.configure(cursor="hand2")
        if danger:
            self.configure(style="danger.TButton")
    
    def select(self):
        self.selected = True
        self.configure(style="light.TButton")

    def deselect(self):
        self.selected = False
        self.configure(style="primary.TButton")

    def is_selected(self) -> bool:
        return self.selected

    def toogle(self):
        if self.selected:
            self.deselect()
        else:
            self.select()

