#store config
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add "/upload" to the base directory
UPLOAD_DIR = os.path.join(BASE_DIR, 'upload')

# Add storage folder / storage
STORAGE = os.path.join(BASE_DIR, 'storage')