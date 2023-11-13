import pdfplumber

def hardware(file):
    try:
        with pdfplumber.open(file) as pdf:
            first_page = pdf.pages[0]  # Assuming you want to crop the first page
            bounding_box = (650, 0, 841, 200)
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
    
