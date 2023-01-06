from stagger import read_tag
from helper import PATH_MUSIC
from helper_path import read_file, write_to_file

#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files):
    global PATH_MUSIC
    count_file_name = 'count.txt'
    try:
        count = int(read_file(count_file_name))
    except:
        count = 0
    
    for _, file_name in enumerate(files):
        count+=1
        music=read_tag(f'{PATH_MUSIC}/{file_name}')
        music.album=str(count)
        music.write()
        
    try:
        write_to_file(count_file_name, str(count))
    except Exception as exception:
        error = f'Failed to write {count_file_name}\nGive write permissions. ({exception})'
        print(error)