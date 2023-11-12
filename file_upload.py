import os

def find_pdf_files(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"The folder path '{folder_path}' does not exist.")
        return None

    # Get the list of files in the folder
    files = os.listdir(folder_path)

    # Filter out only the PDF files
    pdf_files = [file for file in files if file.lower().endswith('.pdf')]

    if not pdf_files:
        print(f"No PDF files found in the folder '{folder_path}'.")
        return None

    return pdf_files