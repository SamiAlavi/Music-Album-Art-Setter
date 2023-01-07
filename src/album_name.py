from stagger import read_tag
from .helper.helper import PATH_MUSIC
from .helper.helper_path import read_file, write_to_file

#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files_names, update_callback):
    global PATH_MUSIC
    count_file_name = 'count.txt'
    try:
        count = int(read_file(count_file_name))
    except:
        count = 0
    
    for _, file_name in enumerate(files_names):
        count+=1
        music=read_tag(f'{PATH_MUSIC}/{file_name}')
        music.album=str(count)
        music.write()
        
    try:
        write_to_file(count_file_name, str(count))
    except Exception as exception:
        error = f'Failed to write {count_file_name}\nGive write permissions. ({exception})'
        update_callback(error)

def start_album_names_runner(files_names, update_callback=print):
    print('\nSetting album names')
    setAlbum(files_names, update_callback)
