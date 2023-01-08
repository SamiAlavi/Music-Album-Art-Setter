if __name__ != '__main__':  
    exit()

from os import listdir
from src.helper.constants import EXTENSIONS_SUPPORTED
from src.helper.helper import setPaths
from src.helper.helper_path import validate_extension

def is_yes_option_selected(option):
    return option == 'y'

def get_input_lowercase(message):
    return input(message).lower()

def get_user_input(message):
    options = ['n', 'y']
    user_input = get_input_lowercase(message)
    while user_input not in options:
        print('Valid input: (N/Y/n/y)')
        user_input = get_input_lowercase(message)
    return is_yes_option_selected(user_input)
    
PATH_MUSIC = 'Music'

find_album_arts = get_user_input('Find album arts? (n/Y) ')
find_music_lyrics = get_user_input('Find music lyrics? (N/y) ')
rename_albums_names = get_user_input('Rename album names? (N/y) ')

setPaths(PATH_MUSIC)
files_names = [file_name for file_name in listdir(PATH_MUSIC) for extension in EXTENSIONS_SUPPORTED if validate_extension(file_name, extension)]
print(f'\nTotal files: {len(files_names)}')

if find_album_arts:
    from src.album_art import start_album_arts_runner
    start_album_arts_runner(files_names)

if find_music_lyrics:
    from src.lyrics import start_lyrics_runner
    start_lyrics_runner(files_names)

if rename_albums_names:
    from src.album_name import start_album_names_runner
    start_album_names_runner(files_names)
