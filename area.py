import pdfplumber

class Area:
    """
    A class for extracting specific areas from a PDF document.

    Parameters:
    - file (str): The path to the PDF file.

    Methods:
    - hardware(show_image=False): Extracts the hardware information area from the first page of the PDF.
    - general_info(show_image=False): Extracts the general information area from the first page of the PDF.
    - job_info(show_image=False): Extracts the job information area from the first page of the PDF.

    These methods provide functionality to crop specific areas from the first page of the PDF document.
    The optional parameter 'show_image' can be set to True to display the cropped image.

    Example:
    ```
    pdf_processor = Area("example.pdf")
    hardware_result = pdf_processor.hardware(show_image=True)
    general_info_result = pdf_processor.general_info()
    job_info_result = pdf_processor.job_info(show_image=True)
    ```

    Note: The '_crop' method is internal to the class and should not be directly accessed by external code.
    """

    def __init__(self, file):
        """
        Initializes an Area object.

        Parameters:
        - file (str): The path to the PDF file.
        """
        self.file = file
        self.pdf = pdfplumber.open(file)
        self.first_page = self.pdf.pages[0]

    def hardware(self, show_image=False):
        """
        Extracts the hardware information area from the first page of the PDF.

        Parameters:
        - show_image (bool): Whether to display the cropped image.

        Returns:
        - pdfplumber.Page: The cropped area as a pdfplumber.Page object.
        """
        bounding_box = (610, 0, 841, 250)
        return self._crop(bounding_box, show_image)

    def general_info(self, show_image=False):
        """
        Extracts the general information area from the first page of the PDF.

        Parameters:
        - show_image (bool): Whether to display the cropped image.

        Returns:
        - pdfplumber.Page: The cropped area as a pdfplumber.Page object.
        """
        bounding_box = (620, 300, 831, 590)
        return self._crop(bounding_box, show_image)
    
    def general_info_data(self):
        second_table_text = self.general_info().extract_text(x_tolerance=1, y_tolerance=1, layout=False)
        lines = second_table_text.split('\n')
        # Create a dictionary to store key-value pairs
        data_dict = {}
        # Find lines containing ':' and create key-value pairs
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)  # Split the line at the first ':' occurrence
                data_dict[key.strip()] = value.strip()
        return data_dict


    def job_info(self, show_image=False):
        """
        Extracts the job information area from the first page of the PDF.

        Parameters:
        - show_image (bool): Whether to display the cropped image.

        Returns:
        - pdfplumber.Page: The cropped area as a pdfplumber.Page object.
        """
        bounding_box = (420, 400, 650, 594)
        return self._crop(bounding_box, show_image)

    def _crop(self, area=None, show_image=False):
        """
        Internal method to crop a specified area from the first page of the PDF.

        Parameters:
        - area (tuple): The bounding box coordinates (left, top, right, bottom) of the area to be cropped.
        - show_image (bool): Whether to display the cropped image.

        Returns:
        - pdfplumber.Page: The cropped area as a pdfplumber.Page object.
        """
        try:
            pdf_crop = self.first_page.crop(bbox=area)

            if show_image:
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
