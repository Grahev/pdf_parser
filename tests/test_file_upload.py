import os
import pytest
import shutil
from file_upload import find_pdf_files 

@pytest.fixture
def setup_temporary_folder():
    # Create a temporary directory for testing
    temp_dir = "tests/temp_test_folder"
    os.makedirs(temp_dir)

    # Create some dummy PDF files
    pdf_files = ["file1.pdf", "file2.pdf", "not_a_pdf.txt"]
    for file in pdf_files:
        with open(os.path.join(temp_dir, file), "w"):
            pass

    yield temp_dir  # Provide the temporary directory path to the test function

    # Teardown: Remove the temporary directory and its contents
    # os.rmdir(temp_dir)
    shutil.rmtree(temp_dir)

def test_find_pdf_files(setup_temporary_folder):
    folder_path = setup_temporary_folder
    pdf_files_list = find_pdf_files(folder_path)

    # Assert that the returned list is not None
    assert pdf_files_list is not None

    # Assert that the expected PDF files are in the list
    expected_pdf_files = ["file1.pdf", "file2.pdf"]
    for pdf_file in expected_pdf_files:
        assert pdf_file in pdf_files_list

    # Assert that the non-PDF file is not in the list
    non_pdf_file = "not_a_pdf.txt"
    assert non_pdf_file not in pdf_files_list

    # Assert that the function handles non-existent folder_path correctly
    invalid_folder_path = "nonexistent_folder"
    result = find_pdf_files(invalid_folder_path)
    assert result is None
