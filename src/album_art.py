from os import listdir
from json import loads
from stagger import read_tag
from .helper.constants import EXTENSION_JPG, FILE_ERROR_ART_GET, FILE_ERROR_ART_SET
from .helper.helper import PATH_MUSIC, PATH_IMAGES, PATH_ERRORS
from .helper.helper import create_directories, get_update_callback, join_paths
from .helper.helper_request import getUrlContent, getParseableSoup
from .helper.helper_path import unhide_directory, append_error_to_file, write_bytes_to_file

#------------------SET ALBUM ART ------------------#
def setArt(music_file_path, image_file_path):
    global PATH_ERRORS
    try:
        music = read_tag(music_file_path)
        music.picture = image_file_path
        music.write()
    except Exception as exception:
        error_file_path = join_paths(PATH_ERRORS, FILE_ERROR_ART_SET)
        error_message = f'Error setting image of {music_file_path}'
        append_error_to_file(error_file_path, error_message, exception)

def setArtRunner(files):
    global PATH_ERRORS, PATH_MUSIC, PATH_IMAGES
    for file_name in files:
        music_file_path = join_paths(PATH_MUSIC, file_name)
        image_file_path = join_paths(PATH_IMAGES, f'{file_name}.{EXTENSION_JPG}')
        setArt(music_file_path, image_file_path)
    unhide_directory(PATH_ERRORS)


#------------------GET ALBUM ART ------------------#
def saveImage(file_name, image_url):
    global PATH_IMAGES
    img_data = getUrlContent(image_url)
    image_file_path = join_paths(PATH_IMAGES, f'{file_name}.{EXTENSION_JPG}')
    write_bytes_to_file(image_file_path, img_data)

def downloadImage(file_name):
    global PATH_ERRORS
    url = 'https://www.bing.com/images/search?q={}&first=1&tsc=ImageBasicHover'
    try:
        param = file_name[:-4]
        soup = getParseableSoup(url, param)
        details = soup.find('a', class_='iusc')['m']
        urlImg = loads(details)['murl']
        saveImage(file_name, urlImg)
        print()
    except Exception as exception:
        print('(ERROR)')
        error_file_path = join_paths(PATH_ERRORS, FILE_ERROR_ART_GET)
        error_message = f'{file_name} image not found'
        append_error_to_file(error_file_path, error_message, exception)

def getAllArts(files_names, update_callback):
    global PATH_IMAGES
    create_directories()
    length = len(files_names)
    for index, file_name in enumerate(files_names):
        image_file_name = f'{file_name}.{EXTENSION_JPG}'
        update_callback(index+1, length, file_name)
        if image_file_name in listdir(PATH_IMAGES): # prevent re-downloading of images with same names
            print()
            continue
        downloadImage(file_name)

def start_album_arts_runner(files_names, dialog=None):
    print('\nGetting album arts')
    update_callback = get_update_callback(dialog)
    getAllArts(files_names, update_callback)
    print('\nSetting album arts')
    setArtRunner(files_names)
