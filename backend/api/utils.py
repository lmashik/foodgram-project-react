import io

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


def create_pdf_shopping_cart(some_list):
    buffer = io.BytesIO()
    cart = Canvas(buffer)
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    cart.setFont('DejaVuSerif', 12)
    height = 800
    wight = 50
    for record in some_list:
        cart.drawString(wight, height, record)
        height -= 20
    cart.showPage()
    cart.save()
    buffer.seek(0)
    return buffer
