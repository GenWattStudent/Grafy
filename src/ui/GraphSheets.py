from __future__ import annotations
import uuid 
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.graph.GraphController import GraphController
from src.graph.GraphModel import GraphModel
from src.ui.OptionMenu import OptionMenu, OptionMenuValue
from ttkbootstrap import ttk
from ttkbootstrap.dialogs import QueryDialog
from src.ui.SwitchButton import SwitchButton

class TabButtonInfo:
    def __init__(self, button: SwitchButton, id: uuid.UUID):
        self.button = button
        self.id = id

class GraphSheets(ttk.Frame):
    def __init__(self, parent, controller: GraphController, *agrs):
        super().__init__(parent, *agrs)
        self.root = parent
        self.controller = controller
        self.graph_sheets: list[GraphModel] = []
        self.tab_buttons: list[TabButtonInfo] = []
        self.current_graph_sheet = None
        # Add button that will add new graph sheet
        self.add_button = ttk.Button(self, text="+", cursor="hand2", command=lambda: self.add_graph_sheet(GraphModel(), f"Graph {len(self.graph_sheets) + 1}"))
        self.add_button.pack(side="left")

    def __len__(self):
        return len(self.graph_sheets)

    def get_graph_by_id(self, id: uuid.UUID) -> GraphModel | None:
        for sheet in self.graph_sheets:
            if sheet.tab_id == id:
                return sheet
        return None
    
    def set_current_graph_sheet(self, model: GraphModel):
        self.current_graph_sheet = model
        for i, sheet in enumerate(self.graph_sheets):
            if sheet.tab_id == model.tab_id:
                self.graph_sheets[i] = model
                break

    def find_button_by_id(self, id: uuid.UUID) -> SwitchButton | None:
        for button in self.tab_buttons:
            if button.id == id:
                return button.button
        return None
    
    def delete_sheet(self, id: uuid.UUID):
        sheet_index = -1
        for i, sheet in enumerate(self.graph_sheets):
            if sheet.tab_id == id:
                self.graph_sheets.pop(i)
                sheet_index = i
                break
        for i, button in enumerate(self.tab_buttons):
            if button.id == id:
                button.button.destroy()
                self.tab_buttons.pop(i)
                break

        if self.current_graph_sheet and self.current_graph_sheet.tab_id == id:
            if sheet_index == 0:
                self.controller.set_model(GraphModel())

            for i, sheet in enumerate(self.graph_sheets):
                if i == sheet_index - 1:
                    self.on_sheet_change(sheet.tab_id)
                    break
        # delete all GraphModels from controllers history with this id
        self.controller.command_history.remove_graphs_with_tab_id(id)
        self.update_add_button_position()

    def edit_sheet_name(self, id: uuid.UUID):
        button = self.find_button_by_id(id)
        if button is not None:
            query = QueryDialog("Enter new name",initialvalue=button.cget('text'), title="Edit Tab Name")
            query.show()
            if query.result is not None:
                button.configure(text=str(query.result))
                self.update_add_button_position()
        
    def update_add_button_position(self):
        total_width = 0
        for tab_button in self.tab_buttons:
            tab_button.button.update()
            total_width += tab_button.button.winfo_width()
        self.add_button.place(x = total_width, y = 0)

    def add_graph_sheet(self, model: GraphModel, title, select=False):
        self.graph_sheets.append(model)
        model.tab_id = uuid.uuid4()
        button = SwitchButton(self, text=title, cursor="hand2", command=lambda: self.on_sheet_change(model.tab_id))
        button.bind("<Button-3>", lambda e: OptionMenu(self.root, [OptionMenuValue("Edit name", lambda: self.edit_sheet_name(model.tab_id)), OptionMenuValue("Delete", lambda: self.delete_sheet(model.tab_id))]).show(e))
        button.pack(side="left")

        if select:
            button.select()

        self.tab_buttons.append(TabButtonInfo(button, model.tab_id))
        self.update_add_button_position()
    
    def on_sheet_change(self, id: uuid.UUID):
        for i, sheet in enumerate(self.graph_sheets):
            if sheet.tab_id == id:
                if self.current_graph_sheet is not None:
                    current_button = self.find_button_by_id(self.current_graph_sheet.tab_id)
                    if current_button is not None:
                        current_button.deselect()
                self.current_graph_sheet = sheet
                self.tab_buttons[i].button.select()
                self.controller.set_model(sheet)
                break
