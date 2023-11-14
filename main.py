import os
from file_upload import find_pdf_files
from separete_page import split_pdf
from area_extractor import hardware
from config import UPLOAD_DIR, TEMP_DIR

files = find_pdf_files(UPLOAD_DIR)

print(UPLOAD_DIR)

for file in files:
    f = os.path.join(UPLOAD_DIR, file)
    hardware(f)