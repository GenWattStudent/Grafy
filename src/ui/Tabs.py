import ttkbootstrap as ttk


class Tabs(ctk.CTkFrame):
    def __init__(self, tabs):
        self.tabs = tabs
        self.tabs_elements = []
        self.current_tab = ""
        self.current_tab_component = None

        for tab in self.tabs:
            button = ctk.CTkButton(self, text=tab["label"], command=lambda tab=tab: self.change_tab(tab["name"]))
            self.tabs_elements.append(button)
        self.change_tab(self.current_tab)

    def change_tab(self, tab_name: str):
        self.current_tab = tab_name
        self.current_tab_component = self.tabs[self.current_tab].draw()
