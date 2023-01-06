from os import path, makedirs
from subprocess import call

def createDirectory(path_directory):
    if not path.exists(path_directory):
        makedirs(path_directory)

def hide_directory(path_directory):
    call(["attrib", "+H", path_directory])

def unhide_directory(path_directory):
    call(["attrib", "-H", path_directory])