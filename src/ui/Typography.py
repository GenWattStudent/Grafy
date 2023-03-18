from enum import Enum
import customtkinter as ctk


class TextType(Enum):
    body = "body"
    h1 = "h1"
    h2 = "h2"
    caption = "caption"


class TextVariant(Enum):
    normal = "normal"
    error = "error"
    success = "success"
    warning = "warning"
    info = "info"


class Typography(ctk.CTkLabel):
    def __init__(
            self, master, text="", type: TextType = TextType.body, variant: TextVariant = TextVariant.normal, **kwargs):
        super().__init__(master, text=text, **kwargs)

        self.set_type(type)
        self.set_variant(variant)

    def set_type(self, type: TextType):
        if type == TextType.body:
            self.configure(font=(None, 12))
        elif type == TextType.h1:
            self.configure(font=(None, 30))
        elif type == TextType.h2:
            self.configure(font=(None, 20))
        elif type == TextType.caption:
            self.configure(font=(None, 10))

    def set_variant(self, variant: TextVariant):
        if variant == TextVariant.normal:
            self.configure(text_color="white")
        elif variant == TextVariant.error:
            self.configure(text_color="red")
        elif variant == TextVariant.success:
            self.configure(text_color="green")
        elif variant == TextVariant.warning:
            self.configure(text_color="yellow")
        elif variant == TextVariant.info:
            self.configure(text_color="blue")
