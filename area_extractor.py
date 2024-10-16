import pdfplumber

def hardware(file):
    try:
        with pdfplumber.open(file) as pdf:
            first_page = pdf.pages[0]  # Assuming you want to crop the first page
            bounding_box = (610, 0, 841, 250)
            pdf_crop = first_page.crop(bbox=bounding_box)
            # img = pdf_crop.to_image()
            # img.show()
            
        # Check if pdf_crop is not None before returning
        if pdf_crop:
            return pdf_crop
        else:
            print("Error: Unable to crop PDF.")
            return None  # Or handle the error in another way
    except Exception as e:
        print(f"Error: {e}")
        return None  # Or handle the error in another way
    
def general_info(file): 
    try:
        with pdfplumber.open(file) as pdf:
            first_page = pdf.pages[0]  # Assuming you want to crop the first page
            # bounding_box = (620, 300, 841, 595)
            bounding_box = (620, 300, 831, 590)
            pdf_crop = first_page.crop(bbox=bounding_box)
            img = pdf_crop.to_image()
            img.show()
            
        # Check if pdf_crop is not None before returning
        if pdf_crop:
            return pdf_crop
        else:
            print("Error: Unable to crop PDF.")
            return None  # Or handle the error in another way
    except Exception as e:
        print(f"Error: {e}")
        return None  # Or handle the error in another way
    
def job_info(file): 
    try:
        with pdfplumber.open(file) as pdf:
            first_page = pdf.pages[0]  # Assuming you want to crop the first page
            # bounding_box = (620, 300, 841, 595)
            bounding_box = (420, 400, 650, 594)
            pdf_crop = first_page.crop(bbox=bounding_box)
            img = pdf_crop.to_image()
            img.show()
            
        # Check if pdf_crop is not None before returning
        if pdf_crop:
            return pdf_crop
        else:
            print("Error: Unable to crop PDF.")
            return None  # Or handle the error in another way
    except Exception as e:
        print(f"Error: {e}")
        return None  # Or handle the error in another way






     
       