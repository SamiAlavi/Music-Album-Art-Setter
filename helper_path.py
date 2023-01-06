from subprocess import call

def hide_directory(path_directory):
    call(["attrib", "+H", path_directory])

def unhide_directory(path_directory):
    call(["attrib", "-H", path_directory])