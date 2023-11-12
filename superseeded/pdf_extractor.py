import pdfplumber
import pandas as pd 
from PyPDF2 import PdfReader, PdfWriter
import io
import re



class Door:
    def __init__(self,job_info,general_info, hardware, structural_opeing):
        self.job_info = job_info
        self.general_info = general_info
        self.hardware = hardware
        self.structural_opening = structural_opeing

    def __str__(self):
        return f"Job no: {self.job_info['job_no']} - {self.job_info['door_no']} | qty: {self.job_info['qty']}"

  


class PDFDataExtractor:
    def __init__(self, input_file):
        self.input_file = input_file
        self.door_data = {}


    def first_page(self):
        with pdfplumber.open(self.input_file) as pdf:
            return pdf.pages[0]
        
    def pages(self):
        with pdfplumber.open(self.input_file) as pdf:
            return len(pdf.pages)

        
    def hardware(self, page):
        #with pdfplumber.open(page) as pdf:
        first_page = page
        bounding_box = (650, 0, 841, 200)
        pdf_crop = first_page.crop(bbox=bounding_box)
        table = pdf_crop.extract_table()
        df = pd.DataFrame(table[1:], columns=table[0])
        return df.to_dict()
    
    def general_info(self, page): 
        first_page = page
        bounding_box = (620, 300, 841, 595)
        second_table = first_page.crop(bbox=bounding_box)
        second_table_text = second_table.extract_text(x_tolerance=1, y_tolerance=1, layout=False)
        second_table_parse = second_table.extract_table()
        lines = second_table_text.split('\n')
        # Create a dictionary to store key-value pairs
        data_dict = {}
        # Find lines containing ':' and create key-value pairs
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)  # Split the line at the first ':' occurrence
                data_dict[key.strip()] = value.strip()
        return data_dict
         
    def job_info(self,page):
        first_page = page
        bounding_box = (420, 400, 650, 595)
        job_section = first_page.crop(bbox=bounding_box)
        job_section_table = job_section.extract_table()
        
        if job_section_table:
            customer = job_section_table[1][0]
            door_no = job_section_table[-1][1].split(':')[-1].strip()
            job_no = job_section_table[-1][0].split('.')[-1].strip()
            rev = job_section_table[-1][-1].split('.')[-1].strip()
            qty = job_section_table[2][0].split('\n')[-1].split(' ')[0]
            job_info = {
                'customer':customer,
                'job_no': job_no,
                'door_no':door_no,
                'qty': qty,
                'revision':rev
            }
            return job_info
        else:
            None
    def vertical_so(self, page):
        pattern_so = r'\b\d{3,4}\sS/O\b'
        pattern_oa_frame = r'\b\d{3,4}\sO/A Frame\b'
        pattern_leaf = r'\b\d{3,4}\sLeaf\b'

        # Read the PDF file


        with open(self.input_file, 'rb') as file:
            pdf_data = io.BytesIO(file.read())

            pdf_reader = PdfReader(pdf_data)

            pdf_writer = PdfWriter()
            page = pdf_reader.pages[page]
            page.rotate(90)  # Rotate the page by 90 degrees clockwise
            pdf_writer.add_page(page)

            rotated_page_data = io.BytesIO()
            pdf_writer.write(rotated_page_data)

        with pdfplumber.open(rotated_page_data) as pdf:
            first_page = pdf.pages[page]
            text = first_page.extract_text(layout=True)


        vertical_so = re.findall(pattern_so, text, re.IGNORECASE)
        vertical_oa_frame = re.findall(pattern_oa_frame, text, re.IGNORECASE)
        vertical_leaf = re.findall(pattern_leaf, text, re.IGNORECASE)

        so = {
            "so": vertical_so[0].split()[0],
            "oa_frame": vertical_oa_frame[0].split()[0],
            "leaf": vertical_leaf[0].split()[0],
        }
        return so
    
    def horizontal_so(self,page):
        pattern_so = r'\b\d{3,4}\sS/O\b'
        pattern_oa_frame = r'\b\d{3,4}\sO/A Frame\b'
        pattern_leaf = r'\b\d{3,4}\sLeaf\b'
        
        with open(self.input_file, 'rb') as file:
            pdf_data = io.BytesIO(file.read())
            pdf_reader = PdfReader(pdf_data)
            pdf_writer = PdfWriter()
            page = pdf_reader.pages[0]
            pdf_writer.add_page(page)
            page_data = io.BytesIO()
            pdf_writer.write(page_data)

        with pdfplumber.open(page_data) as pdf:
            first_page = pdf.pages[0]
            text_h = first_page.extract_text(layout=True)


        horizontal_so = re.findall(pattern_so, text_h, re.IGNORECASE)
        horizontal_oa_frame = re.findall(pattern_oa_frame, text_h, re.IGNORECASE)
        horizontal_leaf = re.findall(pattern_leaf, text_h, re.IGNORECASE)

        so = {
            
            "so": horizontal_so[0].split()[0],
            "oa_frame": horizontal_oa_frame[0].split()[0],
            "leaf": horizontal_leaf #horizontal_leaf[0].split()[0],
            
            
        }
        return so
    
    def structural_opening(self,page):
        structural_opening = {
            "height":self.vertical_so(page),
            "width":self.horizontal_so(page)
        }
        print(f'Structural opening {structural_opening}')
        return structural_opening
        
    def parse(self) -> [Door]:
        data = []
        with pdfplumber.open(self.input_file) as pdf:
            print(pdf.pages)
            
            for page_no in pdf.pages:
                print(page_no)
                p = 0
                door = Door(
                    job_info=self.job_info(page_no),
                    general_info=self.general_info(page_no),
                    hardware=self.hardware(page_no),
                    structural_opeing=self.structural_opening(p)
                )
                data.append(door)
                p += 1
                print(door.structural_opening)
            return data

        


# if __name__ == '__main__':
#     file = 'T6602 combined.pdf'
#     pdf_extractor = PDFDataExtractor(file)
#     doors = pdf_extractor.parse()
#     for i in doors:
#         print(f'\nGeneral info: \n {i.general_info}\n\n Job Info: {i.job_info}\n\n Size: {i.structural_opening}\n\n')
