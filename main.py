if __name__ != '__main__':  
    exit()

import os
from helper import setupSession, setPaths

def validate_extension(query, extension):
    return query.lower().endswith(extension)

def is_flag_yes(flag):
    return flag == 'y'

def get_user_input(message):
    options = ['n', 'y']
    user_input = input(message).lower()
    while user_input not in options:
        print('Valid input: (N/Y/n/y)')
        user_input = input(message).lower()
    return is_flag_yes(user_input)
    
PATH_MUSIC = 'Music'
EXTENSIONS_SUPPORTED = ['.mp3']

find_album_arts = get_user_input('Find album arts? (n/Y) ')
find_music_lyrics = get_user_input('Find music lyrics? (N/y) ')
rename_albums_names = get_user_input('Rename album names? (N/y) ')

setPaths(PATH_MUSIC)
setupSession()
files_names = [file_name for file_name in os.listdir(PATH_MUSIC) for extension in EXTENSIONS_SUPPORTED if validate_extension(file_name, extension)]
print(f'\nTotal files: {len(files_names)}')

if find_album_arts:
    from album_art import getAllArts, setArtRunner
    print('\nGetting album arts')
    getAllArts(files_names)
    setArtRunner(files_names)

if find_music_lyrics:
    from lyrics import getAllLyrics, setLyricsRunner
    print('\nGetting lyrics')
    getAllLyrics(files_names)
    setLyricsRunner(files_names)

if rename_albums_names:
    from album_name import setAlbum
    print('\nGetting album names')
    setAlbum(files_names)
