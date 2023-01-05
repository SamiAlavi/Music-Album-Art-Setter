from os import listdir
from json import loads
from stagger import read_tag
from helper import unhide_directory, createDir
from helper import PATH_MUSIC, PATH_IMAGES, PATH_ERRORS
from helper_request import getUrlContent, getParseableSoup

#------------------SET ALBUM ART ------------------#
def setArt(music_file_path, image_file_path):
    global PATH_ERRORS
    try:
        music = read_tag(music_file_path)
        music.picture = image_file_path
        music.write()
    except Exception as exception:
        set_art_error_file_name = f'{PATH_ERRORS}/errors(setArt).txt'
        with open(set_art_error_file_name, 'a+') as file:
            file.write(f'Error setting image of {music_file_path} ({exception})\n')

def setArtRunner(files):
    global PATH_MUSIC, PATH_IMAGES
    for file_name in files:
        music_file_path = f'{PATH_MUSIC}/{file_name}'
        image_file_path = f'{PATH_IMAGES}/{file_name}.jpg'
        setArt(music_file_path, image_file_path)
    unhide_directory()


#------------------GET ALBUM ART ------------------#
def saveImage(file_name, image_url):
    global PATH_IMAGES
    img_data = getUrlContent(image_url)
    image_file_path = f'{PATH_IMAGES}/{file_name}.jpg'
    with open(image_file_path, 'wb') as file:
        file.write(img_data)

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
        get_image_error_file_name = f'{PATH_ERRORS}/errors(getImage).txt'
        with open(get_image_error_file_name,'a+') as file:
            file.write(f'{file_name} image not found ({exception})\n')

def getAllArts(files_names):
    global PATH_IMAGES
    createDir()
    for index, file_name in enumerate(files_names):
        image_file_name = f'{file_name}.jpg'
        if image_file_name in listdir(PATH_IMAGES): # prevent re-downloading of images with same names
            continue
        print(f'{index+1}) {file_name}', end=' ')
        downloadImage(file_name)