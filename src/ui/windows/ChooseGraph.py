from src.ui.windows.TopLevelWindow import TopLevelWindow
import ttkbootstrap as ttk
from src.ui.GraphSheets import GraphSheets, TabButtonInfo
from src.ui.SwitchButton import SwitchButton
from src.utils.Event import Event
import uuid

class ChooseGraph(TopLevelWindow):
    def __init__(self, parent, title: str, graph_sheets: GraphSheets, **kwargs):
        super().__init__(parent, title, **kwargs)
        self.graph_sheets = graph_sheets
        self.result: list[uuid.UUID] = []
        self.tab_buttons_info = []
        self.select_limit = 2
        self.on_close_event = Event()
        self.create_widgets()
    
    def on_close(self, cb):
        self.on_close_event += cb
    
    def off_close(self, cb):
        self.on_close_event -= cb

    def add_result(self, id: uuid.UUID):
        if id not in self.result:
            self.result.append(id)

    def remove_result_by_id(self, id: uuid.UUID):
        if id in self.result:
            self.result.remove(id)

    def deselect_button_by_id(self, id: uuid.UUID):
        for tab_button_info in self.tab_buttons_info:
            if tab_button_info.id == id:
                tab_button_info.button.deselect()

    def select_button_by_id(self, id: uuid.UUID):
        for tab_button_info in self.tab_buttons_info:
            if tab_button_info.id == id:
                tab_button_info.button.select()
    
    def update_ok_button_state(self):
        if len(self.result) == self.select_limit:
            self.ok_button.config(state="normal")
        else:
            self.ok_button.config(state="disabled")

    def select(self, id: uuid.UUID):
        if len(self.result) == self.select_limit and id not in self.result:
            remove_id = self.result.pop(self.select_limit - 1)
            self.deselect_button_by_id(remove_id)
            self.select_button_by_id(id)

        if id not in self.result:
            self.result.append(id)
            self.select_button_by_id(id)
        else: 
            self.result.remove(id)
            self.deselect_button_by_id(id)
        
        self.update_ok_button_state()
    
    def close(self):
        self.on_close_event(self.result)
        self.destroy()

    def create_widgets(self):
        title_label = ttk.Label(self, text="Choose 2 graphs to compare", font="Helvetica 20 bold")
        title_label.pack(padx=10, pady=10)
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="x", expand=True)

        for info_button in self.graph_sheets.tab_buttons:
            button = SwitchButton(frame, text=info_button.button.cget('text'), command=lambda info=info_button: self.select(info.id))
            button.pack(side="left", padx=10)
            self.tab_buttons_info.append(TabButtonInfo(button, info_button.id))
        
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10)

        self.ok_button = ttk.Button(button_frame, text="OK", command=self.close, cursor="hand2", state = 'disabled')
        self.ok_button.pack(side="left", padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.destroy, cursor="hand2", style="danger.TButton")
        cancel_button.pack(side="left", padx=10)