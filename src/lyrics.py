from os import listdir
from eyed3 import load
from .helper.helper import create_directories, get_update_callback, PATH_MUSIC, PATH_LYRICS, PATH_ERRORS
from .helper.helper_request import getParseableSoup
from .helper.helper_path import unhide_directory, read_file, append_error_to_file, write_to_file

#----------------- SET LYRICS ------------------#
def setLyrics(music_file_path, lyrics_file_path):
    global PATH_ERRORS
    try:
        lyrics = read_file(lyrics_file_path)
        mp3 = load(music_file_path)
        tagg = mp3.tag
        tagg.lyrics.set(lyrics)
        tagg.save(music_file_path)
    except Exception as exception:
        error_file_path = f'{PATH_ERRORS}/errors(setLyrics).txt'
        error_message = f'Error setting lyrics of {music_file_path}'
        append_error_to_file(error_file_path, error_message, exception)

def setLyricsRunner(files_names):
    global PATH_ERRORS, PATH_MUSIC, PATH_LYRICS
    for file_name in files_names:
        music_file_path = f'{PATH_MUSIC}/{file_name}'
        lyrics_file_path = f'{PATH_LYRICS}/{file_name}.txt'
        setLyrics(music_file_path, lyrics_file_path)
    unhide_directory(PATH_ERRORS)
    
#------------------GET LYRICS ------------------#
def writelyrics(file_name, lyrics):
    global PATH_LYRICS
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        lyrics_file_path = f'{PATH_LYRICS}/{file_name}.txt'
        write_to_file(lyrics_file_path, lyrics)

def getYahooReferrerLink(link):
    soup = getParseableSoup(link)
    metaContent = soup.find_all('meta')[-1]['content'] # yahoo uses redirecting
    referrer = metaContent[7:-1]
    return referrer

def downloadLyrics(file_name):
    global PATH_ERRORS
    yahoo_search_url='https://search.yahoo.com/search?p={}%20lyrics'
    azlyrics = 'azlyrics.com%2flyrics' # azlyrics temporary blocks IP address
    letssingit = 'letssingit.com%2f'
    lyricsbox = 'lyricsbox.com%2f'
    nott = '%2flyrics'
    
    param = file_name[:-4]
    soup = getParseableSoup(yahoo_search_url, param)
    classes = " d-ib fz-20 lh-26 td-hu tc va-bot mxw-100p".replace(' ', '.')
    elements_a = soup.select(f'a{classes}')
    
    for element in elements_a:
        href = element['href']
        if azlyrics in href:
            referrer = getYahooReferrerLink(href)
            soup = getParseableSoup(referrer)
            try:
                divs = soup.find_all('div', class_='text-center')[4]
                lyrics = divs.find_all('div')[5].text.strip()
                writelyrics(file_name,lyrics)
            except Exception as exception:
                print(f'(IP Blocked by https://www.azlyrics.com) ({exception})')
            print()
            return
        elif (letssingit in href or lyricsbox in href) and href[-7:]!=nott:
            referrer = getYahooReferrerLink(href)
            soup = getParseableSoup(referrer)
            lyrics = soup.find("div", {"id": "lyrics"}).text.strip()
            writelyrics(file_name,lyrics)
            print()
            return
    
    print('(ERROR)')
    path_error_file = f'{PATH_ERRORS}/errors(getLyrics).txt'
    error_message = f'{file_name} lyrics not found'
    append_error_to_file(path_error_file, error_message, None)

def getAllLyrics(files_names, update_callback):
    global PATH_LYRICS
    create_directories()
    length = len(files_names)
    for index, file_name in enumerate(files_names):
        lyrics_file_name = f'{file_name}.txt'
        update_callback(index+1, length, file_name)
        if lyrics_file_name in listdir(PATH_LYRICS): # prevent re-downloading of lyrics with same names
            print()
            continue
        downloadLyrics(file_name)

def start_lyrics_runner(files_names, dialog=None):    
    print('\nGetting lyrics')
    update_callback = get_update_callback(dialog)
    getAllLyrics(files_names, update_callback)
    print('\nSetting lyrics')
    setLyricsRunner(files_names)
    