from file_upload import find_pdf_files
from separete_page import split_pdf
from config import UPLOAD_DIR, TEMP_DIR

files = find_pdf_files(UPLOAD_DIR)

for file in files:
    split_pdf(file,UPLOAD_DIR, TEMP_DIR)