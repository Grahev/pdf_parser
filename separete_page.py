import os
import pypdf

def split_pdf(file, input_path, output_folder):
    #combine file and input path
    path = os.path.join(input_path, file)
    name = file.split('.')[0]
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    with open(path, 'rb') as file:
        # Create a PdfReader object
        # pdf_reader = PyPDF2.PdfReader(file)
        pdf_reader = pypdf.PdfReader(file)
        
        # Iterate through each page
        for page_number in range(len(pdf_reader.pages)):
            # Create a PdfWriter object
            # pdf_writer = PyPDF2.PdfWriter()
            pdf_writer = pypdf.PdfWriter()

            # Add the current page to the PdfWriter
            pdf_writer.add_page(pdf_reader.pages[page_number])

            # Construct the output file name (original_filename-page_number.pdf)
            # output_file = f"{os.path.splitext(os.path.basename(input_path))[0]}-{page_number + 1:02d}.pdf"
            output_file = f"{name}-{page_number + 1:02d}.pdf"
            
            # Create the output file path
            output_path = os.path.join(output_folder, output_file)

            # Write the current page to the output file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)