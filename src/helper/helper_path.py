import sys
from os import path, makedirs
from subprocess import call
from .constants import PLATFORM_WINDOWS

IS_PLATFORM_WINDOWS = sys.platform == PLATFORM_WINDOWS

def createDirectory(path_directory):
    if not path.exists(path_directory):
        makedirs(path_directory)

def write_to_file(path_file, data, mode='w+'):
    encoding = None if mode.endswith('b') else 'utf-8'
    with open(path_file, mode, encoding=encoding) as file:
        file.write(data)

def write_bytes_to_file(path_file, data):
    write_to_file(path_file, data, mode="wb")

def append_error_to_file(path_error_file, text, exception):
    error_message = f'{text} ({exception})\n'
    write_to_file(path_error_file, error_message, mode='a+')

def read_file(path_file):
    with open(path_file, 'r', encoding='utf-8') as file:
        return file.read()

def hide_directory(path_directory):
    if IS_PLATFORM_WINDOWS:
        call(["attrib", "+H", path_directory])

def unhide_directory(path_directory):
    if IS_PLATFORM_WINDOWS:
        call(["attrib", "-H", path_directory])

def validate_extension(file_name, extension):
    return file_name.lower().endswith(f'.{extension}')

def join_paths(*paths):
    return path.join(*paths)

def is_file(file_path):
    return path.isfile(file_path)

def get_current_absolute_path():
    return path.abspath('.')
