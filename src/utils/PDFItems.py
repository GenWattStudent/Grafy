import os
from PIL import Image
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4

class PDFItem:
    def __init__(self, line_height: int = 0):
        self.x = 0
        self.y = 0
        self.line_height = line_height

class PDFText(PDFItem):
    def __init__(self, text: str, line_height: int, font_size: int, font_name: str, font_color: tuple[int, int, int] = (0, 0, 0), is_centered: bool = False):
        super().__init__(line_height)
        self.text = text
        self.font_size = font_size
        self.font_name = font_name
        self.font_color = font_color
        self.is_centered = is_centered
    
    def draw(self, pdf: pdf_canvas.Canvas):
        if self.is_centered:
            text_width = pdf.stringWidth(self.text, self.font_name, self.font_size)
            self.x = A4[0] / 2 - text_width / 2
  
        pdf.setFillColorRGB(self.font_color[0], self.font_color[1], self.font_color[2], 1)
        pdf.setFont(self.font_name, self.font_size)
        pdf.drawString(self.x, self.y, self.text)
        pdf.setFillColorRGB(0, 0, 0, 1)

class PDFImage(PDFItem):
    def __init__(self, image: Image.Image, line_height: int):
        super().__init__(line_height)
        self.image = image
    
    def draw(self, pdf: pdf_canvas.Canvas):
        self.image.save("temp.png")
        pdf.drawImage('temp.png', self.x, self.y)
        if os.path.exists("temp.png"):
            os.remove("temp.png")
