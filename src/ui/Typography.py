from enum import Enum
import customtkinter as ctk

TextType = Enum('TextType', ['h1', 'h2', 'body', 'caption'])


class Typography(ctk.CTkLabel):
    def __init__(
            self, master, text="", type: TextType = TextType['body'], variant="normal", **kwargs):
        super().__init__(master, text=text, **kwargs)

        self.set_type(type)
        self.set_variant(variant)

    def set_type(self, type):
        if type == "body":
            self.configure(font=(None, 12))
        elif type == "h1":
            self.configure(font=(None, 30))
        elif type == "h2":
            self.configure(font=(None, 20))
        elif type == "caption":
            self.configure(font=(None, 10))

    def set_variant(self, variant):
        if variant == "normal":
            self.configure(text_color="white")
        elif variant == "error":
            self.configure(text_color="red")
        elif variant == "success":
            self.configure(text_color="green")
        elif variant == "warning":
            self.configure(text_color="yellow")
        elif variant == "info":
            self.configure(text_color="blue")
