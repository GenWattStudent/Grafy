import ttkbootstrap as ttk


class TopLevelWindow(ttk.Toplevel):
    def __init__(self, parent, title: str, **kwargs):
        ttk.Toplevel.__init__(self, parent, **kwargs)
        self.title(title)
