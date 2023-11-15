import os
from file_upload import find_pdf_files
from separete_page import split_pdf
from area_extractor import hardware, general_info, job_info
from config import UPLOAD_DIR, TEMP_DIR
from area import Area
from so import StructuralOpening

files = find_pdf_files(UPLOAD_DIR)

print(UPLOAD_DIR)

for file in files:
    split_pdf(file,UPLOAD_DIR, TEMP_DIR)

single_files = find_pdf_files(TEMP_DIR)

for file in single_files:
    f = os.path.join(TEMP_DIR, file)
    area = Area(f)
    d = area.general_info_data()
    so = StructuralOpening(f)
    print(area.general_info_data(), so.horizontal_so(), so.vertical_so())
    