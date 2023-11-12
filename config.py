#store config
import os
import pathlib

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = pathlib.Path(__file__).parent.resolve()

PROJECT_DIR = os.path.dirname(BASE_DIR)

# Add "/upload" to the base directory
UPLOAD_DIR = os.path.join(BASE_DIR, 'upload')

TEMP_DIR = os.path.join(BASE_DIR, 'temp')

# Add storage folder / storage
STORAGE = os.path.join(BASE_DIR, 'storage')