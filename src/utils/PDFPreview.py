from reportlab.lib.pagesizes import A4
from PIL import Image, ImageTk
from src.utils.PDFItems import PDFText, PDFImage
import ttkbootstrap as tkk

class PDFPreview(tkk.Canvas):
    def __init__(self, master, width=300, height=700, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.items = []
        self.width = width
        self.height = height
        self.line_height = 0
        self.header_font_size = 24
        self.header_2_font_size = 18
        self.body_font_size = 12
        self.caption_font_size = 10
        self.font_name = "Helvetica"
        self.font_name_bold = "Helvetica-Bold"
        self.page_count = 1
        self.margin_x = 40
        self.margin_y = 40
        self.page_size = A4
        self.configure(bg="white")
    
    def resize_pdf_to_fit(self):
        # scale all to fit pdf page that is A4 but canvas can be smaller or bigger 
        
        # scale factor
        scale_factor = min(self.width / self.page_size[0], self.height / self.page_size[1])

        # scale all items
        for item in self.items:
            self.margin_x = 40 * scale_factor
            self.margin_y = 40 * scale_factor
            item.x *= scale_factor
            item.y *= scale_factor
            if isinstance(item, PDFText):
                item.font_size = int(item.font_size * scale_factor)
            elif isinstance(item, PDFImage):
                item.image.resize((int(item.image.width * scale_factor), int(item.image.height * scale_factor)), Image.ANTIALIAS)

    def add_header_1(self, text: str):
        self.items.append(PDFText(text, self.body_font_size + 20, self.body_font_size, self.font_name_bold))
        self.draw()
    
    def add_header_2(self, text: str):
        self.items.append(PDFText(text, self.body_font_size + 10, self.body_font_size, self.font_name_bold))
        self.draw()
    
    def add_text(self, text: str):
        self.items.append(PDFText(text, self.body_font_size + 4, self.body_font_size, self.font_name))
        self.draw()
    
    def add_image(self, image: Image.Image):
        self.items.append(PDFImage(image, self.body_font_size))
        self.draw()
    
    def draw_text(self, elemnt: PDFText):
        self.create_text(elemnt.x, elemnt.y, text=elemnt.text, font=(elemnt.font_name, elemnt.font_size), anchor="nw", fill='black')

    def draw_image(self, elemnt: PDFImage):
        print(elemnt.image)
        self.create_image(elemnt.x, elemnt.y, image=ImageTk.PhotoImage(elemnt.image), anchor="nw")

    def draw(self):
        self.delete("all")
        # self.resize_pdf_to_fit()
        # draw all items
        line_height = 0
        x = self.margin_x
        y = self.margin_y
        for item in self.items:
            if isinstance(item, PDFText):
                item.x = x
                item.y = y + line_height + item.line_height
                y +=line_height
                line_height = item.line_height
                self.draw_text(item)
            elif isinstance(item, PDFImage):
                item.x = x
                item.y = y + line_height
                y += item.line_height + item.image.height
                line_height = line_height
                self.draw_image(item)