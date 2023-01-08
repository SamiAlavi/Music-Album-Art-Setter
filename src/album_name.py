from stagger import read_tag
from .helper.constants import FILE_COUNT
from .helper.helper import PATH_MUSIC
from .helper.helper import join_paths
from .helper.helper_path import read_file, write_to_file

#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files_names, update_callback):
    global PATH_MUSIC
    try:
        count = int(read_file(FILE_COUNT))
    except:
        count = 0
    
    for _, file_name in enumerate(files_names):
        count += 1
        file_path = join_paths(PATH_MUSIC, file_name)
        music = read_tag(file_path)
        music.album = str(count)
        music.write()
        
    try:
        write_to_file(FILE_COUNT, str(count))
    except Exception as exception:
        error = f'Failed to write {FILE_COUNT}\nGive write permissions. ({exception})'
        update_callback(error)

def start_album_names_runner(files_names, update_callback=print):
    print('\nSetting album names')
    setAlbum(files_names, update_callback)
