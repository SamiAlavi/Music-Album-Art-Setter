from os import listdir
from json import loads
from stagger import read_tag
from helper import create_directories
from helper import PATH_MUSIC, PATH_IMAGES, PATH_ERRORS
from helper_request import getUrlContent, getParseableSoup
from helper_path import unhide_directory, append_error_to_file, write_bytes_to_file

#------------------SET ALBUM ART ------------------#
def setArt(music_file_path, image_file_path):
    global PATH_ERRORS
    try:
        music = read_tag(music_file_path)
        music.picture = image_file_path
        music.write()
    except Exception as exception:
        error_file_path = f'{PATH_ERRORS}/errors(setArt).txt'
        error_message = f'Error setting image of {music_file_path}'
        append_error_to_file(error_file_path, error_message, exception)

def setArtRunner(files):
    global PATH_ERRORS, PATH_MUSIC, PATH_IMAGES
    for file_name in files:
        music_file_path = f'{PATH_MUSIC}/{file_name}'
        image_file_path = f'{PATH_IMAGES}/{file_name}.jpg'
        setArt(music_file_path, image_file_path)
    unhide_directory(PATH_ERRORS)


#------------------GET ALBUM ART ------------------#
def saveImage(file_name, image_url):
    global PATH_IMAGES
    img_data = getUrlContent(image_url)
    image_file_path = f'{PATH_IMAGES}/{file_name}.jpg'
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
        error_file_path = f'{PATH_ERRORS}/errors(getImage).txt'
        error_message = f'{file_name} image not found'
        append_error_to_file(error_file_path, error_message, exception)

def getAllArts(files_names):
    global PATH_IMAGES
    create_directories()
    for index, file_name in enumerate(files_names):
        image_file_name = f'{file_name}.jpg'
        if image_file_name in listdir(PATH_IMAGES): # prevent re-downloading of images with same names
            continue
        print(f'{index+1}) {file_name}', end=' ')
        downloadImage(file_name)

def start_album_arts_runner(files_names):
    print('\nGetting album arts')
    getAllArts(files_names)
    print('\nSetting album arts')
    setArtRunner(files_names)
