import requests
from bs4 import BeautifulSoup
from stagger import read_tag
from os import listdir
from eyed3 import load
import os
from subprocess import call
from urllib.parse import quote

SESSION = None
PATH_MUSIC = None
PATH_IMAGES = None
PATH_LYRICS = None
PATH_ERRORS = None

def setupSession():
    global SESSION
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    SESSION = requests.Session()
    SESSION.headers = headers

def encodeUrl(url):
    return quote(url) # urllib.parse.quote()

def getUrlContent(url, param=None):
    global SESSION
    if param:
        param = encodeUrl(param)
        url = url.format(param)
    return SESSION.get(url).content

def getParseableSoup(url, param=None):
    html = getUrlContent(url, param)
    return BeautifulSoup(html, "html.parser")

def createDir():
    global PATH_IMAGES, PATH_LYRICS, PATH_ERRORS
    for path in [PATH_ERRORS, PATH_IMAGES, PATH_LYRICS]:
        if not os.path.exists(path):
            os.makedirs(path)
    hide_directory()    

def hide_directory():
    global PATH_ERRORS
    call(["attrib", "+H", PATH_ERRORS])

def unhide_directory():
    global PATH_ERRORS
    call(["attrib", "-H", PATH_ERRORS])

def setPaths(path):
    global PATH_MUSIC, PATH_IMAGES, PATH_LYRICS, PATH_ERRORS
    PATH_MUSIC = path
    PATH_ERRORS = f'{path}/downloads'   
    PATH_IMAGES = f'{path}/downloads/images'
    PATH_LYRICS = f'{path}/downloads/lyrics'


            
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

#----------------- SET LYRICS ------------------#
def setLyrics(music_file_path, lyrics_file_path):
    global PATH_ERRORS
    try:
        with open(lyrics_file_path,'r', encoding='utf-8') as file:
            lyrics = file.read()
        mp3 = load(music_file_path)
        tagg = mp3.tag
        tagg.lyrics.set(lyrics)
        tagg.save(music_file_path)
    except Exception as exception:
        set_lyrics_error_file_name = f'{PATH_ERRORS}/errors(setLyrics).txt'
        with open(set_lyrics_error_file_name,'a+') as file:
            file.write(f'Error setting lyrics of {music_file_path} ({exception})\n')

def setLyricsRunner(files_names):
    global PATH_MUSIC, PATH_LYRICS
    for file_name in files_names:
        music_file_path = f'{PATH_MUSIC}/{file_name}'
        lyrics_file_path = f'{PATH_LYRICS}/{file_name}.txt'
        setLyrics(music_file_path, lyrics_file_path)
    unhide_directory()
    
#------------------GET LYRICS ------------------#
def writelyrics(file_name, lyrics):
    global PATH_LYRICS
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        lyrics_file_path = f'{PATH_LYRICS}/{file_name}.txt'
        with open(lyrics_file_path,'w', encoding='utf-8') as file:
            file.write(lyrics)

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
    get_lyrics_error_file_name = f'{PATH_ERRORS}/errors(getLyrics).txt'
    with open(get_lyrics_error_file_name, 'a', encoding='utf-8') as file:
        file.write(f'{file_name} lyrics not found\n')

def getAllLyrics(files_names):
    global PATH_LYRICS
    createDir()
    for index, file_name in enumerate(files_names):
        lyrics_file_name = f'{file_name}.txt'
        if lyrics_file_name in listdir(PATH_LYRICS): # prevent re-downloading of lyrics with same names
            continue
        print(f'{index+1}) {file_name}', end=' ')
        downloadLyrics(file_name)
