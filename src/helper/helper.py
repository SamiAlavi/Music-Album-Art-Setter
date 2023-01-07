from .helper_path import hide_directory, createDirectory

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
    PATH_ERRORS = f'{path}/downloads'   
    PATH_IMAGES = f'{path}/downloads/images'
    PATH_LYRICS = f'{path}/downloads/lyrics'

def get_update_callback(dialog):
    if dialog:
        return lambda index, length, file_name: dialog.update_progress(index, length, file_name)
    else:
        return lambda index, _, file_name: print(f'{index}) {file_name}', end=' ')
