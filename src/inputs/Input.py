import customtkinter as ctk
from src.ui.Typography import Typography, TextType, TextVariant
from src.utils.Event import Event


class Input(ctk.CTkEntry):
    def __init__(self, master, label_text="", default_value="", rules={}, filtr=None, **kwargs):
        self.rules = rules
        self.last_correct_value = default_value
        self.filtr = filtr
        self.text_var = ctk.StringVar()
        self.text_var.trace("w", lambda name, index, mode, sv=self.text_var: self.handle_change(sv))

        self.frame = ctk.CTkFrame(master, fg_color="transparent")
        self.frame.pack(fill="x")

        super().__init__(master=self.frame, textvariable=self.text_var,  **kwargs)

        self.change_event = Event()

        self.label = Typography(self.frame, text=label_text)
        self.label.pack(anchor="w", padx=10, pady=5)

        self.insert(0, default_value)
        self.bind("<FocusOut>", lambda event: self.hide_error())
        self.pack(anchor="w", padx=10, fill="x")

    def set_input_value(self, value: str):
        self.delete(0, "end")
        self.insert(0, value)

    def handle_change(self, value):
        value = value.get()

        if self.filtr:
            value = self.filtr(value)

        if not value:
            return

        if self.validate(value):
            self.last_correct_value = value
            return self.change_event(value)

        self.set_input_value(self.last_correct_value)

    def show_error(self, error_message):
        self.error_label = Typography(self.frame, text=error_message, type=TextType.caption, variant=TextVariant.error)
        self.error_label.pack(anchor="w", padx=10, pady=5)

    def hide_error(self):
        if hasattr(self, 'error_label') and self.error_label:
            self.error_label = self.error_label.destroy()

    def validate(self, value) -> bool:
        self.hide_error()

        error_message = ""
        for rule in self.rules:
            if not self.rules[rule](value):
                error_message += self.rules[rule].error_message + ", \n"

        if error_message:
            error_message = error_message[:-3] + "."
            self.show_error(error_message)
            return False
        return True

    def on_change(self, callback):
        self.change_event += callback

    def off_change(self, callback):
        self.change_event -= callback
