import ttkbootstrap as ttk
from src.ui.Typography import Typography
from src.utils.Event import Event


class Input(ttk.Entry):
    def __init__(self, master, label_text="", default_value="", rules={}, filtr=None, **kwargs):
        self.rules = rules
        self.last_correct_value = default_value
        self.filtr = filtr
        self.text_var = ttk.StringVar()
        self.text_var.trace("w", lambda name, index, mode, sv=self.text_var: self.handle_change(sv))

        self.frame = ttk.Frame(master)
        self.frame.pack(fill="x", anchor="w")

        self.error_labels: list[ttk.Label] = []

        super().__init__(master=self.frame, textvariable=self.text_var,  **kwargs)

        self.change_event = Event()

        self.label = Typography(self.frame, text=label_text)
        self.label.pack(anchor="w", padx=10, pady=5)

        self.insert(0, default_value)
        self.bind("<FocusOut>", lambda event: self.hide_error())
        self.bind("<Configure>", self.resize)
        self.pack(anchor="w", padx=10, fill="x")

    def get(self):
        return self.text_var.get()
    
    def resize(self, event):
        print(self.winfo_width())
        for label in self.error_labels:
            label.configure(wraplength=self.winfo_width() - 20)

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

    def hide_error(self):
        error_labels_copy = list(self.error_labels)
        for label in error_labels_copy:
            self.error_labels.remove(label)
            label.destroy()

    def validate(self, value) -> bool:
        self.hide_error()

        for rule in self.rules:
            if not self.rules[rule](value):
                label = Typography(self.frame, text=self.rules[rule].error_message + ",", style = "DANGER.TLabel", wraplength=self.winfo_width() - 20)
                label.pack(anchor="w", padx=10)
                self.error_labels.append(label)

        if len(self.error_labels) > 0:
            self.error_labels[-1].configure(text=self.error_labels[-1].cget("text")[:-1] + ".")
            return False
        return True

    def on_change(self, callback):
        self.change_event += callback

    def off_change(self, callback):
        self.change_event -= callback
