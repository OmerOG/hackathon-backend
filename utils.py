import os
from zipfile import ZipFile

def safe_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_zip_file(path, file_paths):
    with ZipFile(path + ".zip", "w") as zipObj:
            for filename in file_paths:
                zipObj.write(filename, os.path.basename(filename))

def safe_remove_file(path):
    if os.path.exists(path):
        os.remove(path)