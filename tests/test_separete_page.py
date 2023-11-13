import os
import pytest
import pypdf
from config import TEST_UPLOAD_DIR, TEST_TEMP_DIR

from separete_page import split_pdf

# Sample PDF file for testing
SAMPLE_PDF = 'files\T6099.pdf'

@pytest.fixture
def setup_teardown():
    # Set up: Create a temporary directory for testing
    # temp_dir = 'tests/temp_test_folder'
    temp_dir = TEST_TEMP_DIR
    os.makedirs(temp_dir)

    yield temp_dir

    # Teardown: Remove the temporary directory and its contents after testing
    for file in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, file)
        os.remove(file_path)
    os.rmdir(temp_dir)


def test_split_pdf(setup_teardown):
    input_path = os.path.dirname(os.path.abspath(__file__))  # Use the directory where the test file is located
    # input_path = TEST_TEMP_DIR  # Use the directory where the test file is located
    # output_folder = setup_teardown
    output_folder = TEST_TEMP_DIR

    # Call the function to split the sample PDF
    split_pdf(SAMPLE_PDF, input_path, output_folder)

    # Check if the expected number of output files is created
    expected_output_files = len(pypdf.PdfReader(os.path.join(input_path, SAMPLE_PDF)).pages)
    actual_output_files = len(os.listdir(output_folder))
    assert actual_output_files == expected_output_files

    # Check if each output file is created successfully
    # for page_number in range(expected_output_files):
    #     output_file = f"{os.path.splitext(SAMPLE_PDF)[0]}-{page_number + 1:02d}.pdf"
    #     output_path = os.path.join(output_folder, output_file)
    #     assert os.path.isfile(output_path)

    # Additional checks can be added based on specific requirements of your function
