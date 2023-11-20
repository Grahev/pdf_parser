import os
from file_upload import find_pdf_files
from separete_page import split_pdf
from area_extractor import hardware, general_info, job_info
from config import UPLOAD_DIR, TEMP_DIR
from area import Area
from so import StructuralOpening
from models import DoorData

files = find_pdf_files(UPLOAD_DIR)

print(UPLOAD_DIR)

for file in files:
    split_pdf(file,UPLOAD_DIR, TEMP_DIR)

single_files = find_pdf_files(TEMP_DIR)

for file in single_files:
    f = os.path.join(TEMP_DIR, file)

    # Assuming Area and StructuralOpening classes are defined
    area = Area(f)
    so = StructuralOpening(f)

    # Create a dictionary with the combined data
    combined_data = {
        **area.job_info_data(),
        **area.general_info_data(),
        **so.horizontal_so(),
        **so.vertical_so()
    }

    # Create a DoorData instance from the dictionary
    door_instance = DoorData.from_dict(combined_data)

    # Now you can use door_instance for further operations
    print(door_instance.customer)
    print(door_instance.door_details)
    print(door_instance.order_details)

    # Save to SQLite database
    door_instance.save_to_database()

    