import os
import io


from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

TEMPLATE_FILE_NAME = 'pass.pdf'     # file to be used as template
LOCATION = 'cards/'                 # the directory where all of the cards be stored

FONT = 'Arial'                      # Font of the text to be written on the card
FONT_SIZE = 23                      # Size of the text

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf')) # Registers a font


class Card:
    def __init__(self, size_x=90*mm, size_y=58*mm, loc_x=66*mm, loc_y=39*mm, digits=3, start=1):
        self.number = start
        self.digits = digits
        self.size = size_x, size_y
        self.text_location = loc_x, loc_y

    def get_the_number(self):
        return self.number

    def convert_number_to_text(self):
        length = len(str(self.number))
        return '0' * (self.digits - length) + str(self.number)

    def increase_number(self):
        self.number += 1

    def blank_pdf_with_text(self, packet):
        number = self.convert_number_to_text()
        can = canvas.Canvas(packet, pagesize=self.size)
        can.setFont(FONT, FONT_SIZE)
        can.setFillColorRGB(0.5, 0, 0)
        can.drawString(self.text_location[0], self.text_location[1], number)

        can.save()

    def get_output_filename(self):
        number = self.convert_number_to_text()
        file_name = LOCATION + 'card' + number + '.pdf'
        return file_name

    def create_output_file(self, output):
        file_name = self.get_output_filename()
        output_stream = open(file_name, "wb")
        output.write(output_stream)
        output_stream.close()

    def build_pdf_to_merge(self):
        packet = io.BytesIO()

        self.blank_pdf_with_text(packet)

        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(open(TEMPLATE_FILE_NAME, 'rb'))
        output = PdfFileWriter()

        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)

        page = existing_pdf.getPage(1)
        output.addPage(page)

        self.create_output_file(output)

    def build_batch(self, n):
        for i in range(n):
            self.build_pdf_to_merge()
            self.increase_number()

    def merge_all_files(self, location=LOCATION):
        merger = PdfFileMerger()
        for pdf_file in os.listdir(location):
            if pdf_file.endswith('.pdf'):
                file_name = location + pdf_file
                merger.append(PdfFileReader(open(file_name, 'rb')))

        merger.write('merged_files.pdf')


if __name__ == '__main__':
    card = Card()
    card.build_pdf_to_merge()
    card.build_batch(501)
    card.merge_all_files()
