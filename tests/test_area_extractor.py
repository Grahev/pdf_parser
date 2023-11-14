import pytest
from area_extractor import hardware  


# Assume you have a sample PDF file for testing
# SAMPLE_PDF = "tests\\files\\T6099.pdf"
SAMPLE_PDF = "tests\\files\\TR0943 combined.pdf"

def test_hardware_successful_crop():
    # Assuming your sample PDF can be successfully cropped
    result = hardware(SAMPLE_PDF)
    assert result is not None
    # Add more assertions based on the expected behavior of your function

def test_hardware_failed_crop():
    # Test the case where cropping fails (e.g., invalid PDF or bounding box)
    result = hardware('invalid_file')
    assert result is None
    # Add more assertions based on the expected behavior of your function

# Add more tests as needed