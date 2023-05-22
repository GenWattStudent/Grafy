from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
from src.utils.PDFItems import PDFText, PDFImage

class PDFBuilder(pdf_canvas.Canvas):
    def __init__(self, filename, pagesize=A4, bottomup=1, pageCompression=None, invariant=None, verbosity=0, encrypt=None, cropMarks=None, pdfVersion=None, enforceColorSpace=None, initialFontName=None, initialFontSize=None, initialLeading=None, cropBox=None, artBox=None, trimBox=None, bleedBox=None, lang=None):
        super().__init__(filename, pagesize, bottomup, pageCompression, invariant, verbosity, encrypt, cropMarks, pdfVersion, enforceColorSpace, initialFontName, initialFontSize, initialLeading, cropBox, artBox, trimBox, bleedBox, lang)
        self.margin_x = 40
        self.margin_y = 40
        self.sequence = []
        self.page_size: tuple[int, int] = pagesize
        self.line_height = 0
        self.header_font_size = 24
        self.header_2_font_size = 18
        self.body_font_size = 12
        self.caption_font_size = 10
        self.font_name = "Helvetica"
        self.font_name_bold = "Helvetica-Bold"
        self.page_count = 1
    
    def set_filename(self, filename: str):
        self._filename = filename

    def set_header_font_size(self, size: int):
        self.header_font_size = size
    
    def set_header_2_font_size(self, size: int):
        self.header_2_font_size = size
    
    def set_body_font_size(self, size: int):
        self.body_font_size = size

    def set_caption_font_size(self, size: int):
        self.caption_font_size = size
    
    def set_margin(self, x: int, y: int):
        self.margin_x = x
        self.margin_y = y
    
    def resize_image(self, image: Image.Image, width: float, height: float) -> Image.Image:
        scale_width = width / image.width
        scale_height = height / image.height

        scale_factor = min(scale_width, scale_height)

        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)

        return image.resize((new_width, new_height), Image.ANTIALIAS)

    def add_page_break(self):
        self.showPage()
    
    def add_body(self, text: str, font_color: tuple[int, int, int] = (0, 0, 0), is_centered: bool = False):
        self.sequence.append(PDFText(text, self.body_font_size + 4, self.body_font_size, self.font_name_bold, font_color, is_centered))
    
    def add_header_1(self, text: str, font_color: tuple[int, int, int] = (0, 0, 0), is_centered: bool = False):
        self.sequence.append(PDFText(text, self.header_font_size + 12, self.header_font_size, self.font_name, font_color, is_centered))
    
    def add_header_2(self, text: str):
        self.sequence.append(PDFText(text, self.header_2_font_size + 12, self.header_2_font_size, self.font_name))
    
    def add_caption(self, text: str):
        self.sequence.append(PDFText(text, self.caption_font_size + 3, self.caption_font_size, self.font_name))
    
    def add_image(self, image: Image.Image):
        img = self.resize_image(image, self.page_size[0] - self.margin_x * 2, self.page_size[1] - self.margin_y * 2)
        self.sequence.append(PDFImage(img, 10))
    
    def build(self):
        x = self.margin_x
        y = self.page_size[1]  - self.margin_y
        line_height = 0
        for item in self.sequence:
            if isinstance(item, PDFText):
                if y - line_height - item.line_height <= self.margin_y:
                    self.add_page_break()
                    x = self.margin_x
                    y = self.page_size[1]  - self.margin_y
                    line_height = 0
                item.x = x
                item.y = y - line_height - item.line_height
                item.draw(self)
                y -= line_height
                line_height = item.line_height
            elif isinstance(item, PDFImage):
                if y - line_height - item.line_height - item.image.height <= self.margin_y:
                    self.add_page_break()
                    x = self.margin_x
                    y = self.page_size[1]  - self.margin_y
                    line_height = 0
                item.x = x
                item.y = y - item.image.height - line_height - item.line_height
                item.draw(self)
                y -= line_height - item.image.height
                line_height = item.line_height
        self.add_page_break()