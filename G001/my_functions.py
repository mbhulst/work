# collection of functions

import os

def get_file_path(file_name: str):
        
    cwd = os.getcwd()
    file_path = cwd + '\\input\\' + file_name

    return file_path
