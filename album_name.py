from stagger import read_tag
from helper import PATH_MUSIC

#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files):
    global PATH_MUSIC
    count_file_name = 'count.txt'
    try:
        with open(count_file_name, 'r') as file:
            count=int(file.read())
    except:
        count=0
    
    for index, file_names in enumerate(files):
        count+=1
        music=read_tag(f'{PATH_MUSIC}/{file_names}')
        music.album=str(count)
        music.write()
        
    try:
        with open(count_file_name, 'w') as file:
            file.write(str(count))
    except Exception as exception:
        error = f'Failed to write {count_file_name}\nGive write permissions. ({exception})'
        print(error)