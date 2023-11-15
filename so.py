import io
import re
import pdfplumber
from pypdf import PdfReader, PdfWriter

class StructuralOpening:
    def __init__(self, file):
        self.file = file
        self.pdf = pdfplumber.open(file)
        self.first_page = self.pdf.pages[0]


    def _rotate(self):
        """Rotate page on 90 degrees clockwise"""
        with open(self.file, 'rb') as file:
            pdf_data = io.BytesIO(file.read())
            pdf_reader = PdfReader(pdf_data)
            pdf_writer = PdfWriter()

            page = pdf_reader.pages[0]
            page.rotate(90)  # Rotate the page by 90 degrees clockwise
            pdf_writer.add_page(page)
            rotated_page_data = io.BytesIO()
            pdf_writer.write(rotated_page_data)

            return rotated_page_data.getvalue()
        
    def vertical_so(self):
        rotated_data = self._rotate()

        # Open the rotated PDF data
        with io.BytesIO(rotated_data) as rotated_file:
            rotated_pdf = pdfplumber.open(rotated_file)
            rotated_first_page = rotated_pdf.pages[0]

            pattern_so = r'\b\d{3,4}\sS/O\b'
            pattern_oa_frame = r'\b\d{3,4}\sO/A Frame\b'
            pattern_leaf = r'\b\d{3,4}\sLeaf\b'

            text_v = rotated_first_page.extract_text(layout=True)
          

            vertical_so = re.findall(pattern_so, text_v, re.IGNORECASE)
            vertical_oa_frame = re.findall(pattern_oa_frame, text_v, re.IGNORECASE)
            vertical_leaf = re.findall(pattern_leaf, text_v, re.IGNORECASE)

            so = {
                "so": vertical_so[0].split()[0] if vertical_so else None,
                "oa_frame": vertical_oa_frame[0].split()[0] if vertical_oa_frame else None,
                "leaf": vertical_leaf[0].split()[0] if vertical_leaf else None,
            }
            return so



    def horizontal_so(self):
        pattern_so = r'\b\d{3,4}\sS/O\b'
        pattern_oa_frame = r'\b\d{3,4}\sO/A Frame\b'
        pattern_leaf = r'\b\d{3,4}\sLeaf\b'
        
        text_h = self.first_page.extract_text(layout=True)

        horizontal_so = re.findall(pattern_so, text_h, re.IGNORECASE)
        horizontal_oa_frame = re.findall(pattern_oa_frame, text_h, re.IGNORECASE)
        horizontal_leaf = re.findall(pattern_leaf, text_h, re.IGNORECASE)

        so = {
            
            "so": horizontal_so[0].split()[0],
            "oa_frame": horizontal_oa_frame[0].split()[0],
            "leaf": horizontal_leaf #horizontal_leaf[0].split()[0],    
        }
        return so
    
    def rotated_so(self):
        pattern_so = r'\b\d{3,4}\sS/O\b'
        pattern_oa_frame = r'\b\d{3,4}\sO/A Frame\b'
        pattern_leaf = r'\b\d{3,4}\sLeaf\b'
        
        rotated_text = self.first_page_rotate.extract_text(layout=True)

        rotated_horizontal_so = re.findall(pattern_so, rotated_text, re.IGNORECASE)
        rotated_horizontal_oa_frame = re.findall(pattern_oa_frame, rotated_text, re.IGNORECASE)
        rotated_horizontal_leaf = re.findall(pattern_leaf, rotated_text, re.IGNORECASE)

        rotated_so = {
            "so": rotated_horizontal_so[0].split()[0],
            "oa_frame": rotated_horizontal_oa_frame[0].split()[0],
            "leaf": rotated_horizontal_leaf # rotated_horizontal_leaf[0].split()[0],    
        }
        return rotated_so