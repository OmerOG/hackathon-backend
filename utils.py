import os


def safe_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)