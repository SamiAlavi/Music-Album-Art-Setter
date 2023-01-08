from .helper_path import hide_directory, createDirectory, join_paths

PATH_MUSIC = None
PATH_IMAGES = None
PATH_LYRICS = None
PATH_ERRORS = None

def create_directories():
    global PATH_IMAGES, PATH_LYRICS, PATH_ERRORS
    for path_directory in (PATH_ERRORS, PATH_IMAGES, PATH_LYRICS):
        createDirectory(path_directory)
    hide_directory(PATH_ERRORS)

def setPaths(path):
    global PATH_MUSIC, PATH_IMAGES, PATH_LYRICS, PATH_ERRORS
    PATH_MUSIC = path
    PATH_ERRORS = join_paths(path, 'downloads')
    PATH_IMAGES = join_paths(PATH_ERRORS, 'images')
    PATH_LYRICS = join_paths(PATH_ERRORS, 'lyrics')

def get_update_callback(dialog):
    if dialog:
        return lambda index, length, file_name: dialog.update_progress(index, length, file_name)
    else:
        return lambda index, _, file_name: print(f'{index}) {file_name}', end=' ')