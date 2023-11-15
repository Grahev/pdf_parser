import pytest
from area import Area
import os

# Assume you have a sample PDF file for testing
# SAMPLE_PDF = "files\TR0943 combined.pdf"
SAMPLE_PDF = os.path.join("tests", "files", "TR0943 combined.pdf")

@pytest.fixture
def pdf_processor():
    return Area(SAMPLE_PDF)

def test_hardware_successful_crop(pdf_processor):
    # Assuming your sample PDF can be successfully cropped
    result = pdf_processor.hardware()
    assert result is not None
    # Add more assertions based on the expected behavior of your function

def test_hardware_failed_crop():
    # Test the case where cropping fails (e.g., invalid PDF or bounding box)
    invalid_pdf_path = 'tests/files/invalid_file.pdf'  # Adjust the path to an invalid file

    with pytest.raises(FileNotFoundError):
        pdf_processor = Area(invalid_pdf_path)
        result = pdf_processor.hardware()
    # Add more assertions based on the expected behavior of your function

# Add more tests as needed
