import os


def folder_exists(path):
    return os.path.exists(path) and os.path.isdir(path)
