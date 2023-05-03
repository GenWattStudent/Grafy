from enum import Enum
import ttkbootstrap as ttk


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


class Typography(ttk.Label):
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
        pass
