import customtkinter as ctk


class TopLevelWindow(ctk.CTkToplevel):
    def __init__(self, parent, title: str, **kwargs):
        ctk.CTkToplevel.__init__(self, parent, **kwargs)
        self.title(title)
