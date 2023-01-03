import requests
from bs4 import BeautifulSoup
from stagger import read_tag
from os import listdir
from eyed3 import load
import os
from subprocess import call
from json import loads
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

#------------------SET ALBUM ART ------------------#
def setArt(music_file_path, image_file_path):
    global PATH_ERRORS
    try:
        music = read_tag(music_file_path)
        music.picture = image_file_path
        music.write()
    except:
        set_art_error_file_name = f'{PATH_ERRORS}/errors(setArt).txt'
        with open(set_art_error_file_name, 'a+') as file:
            file.write(f'Error setting image of {music_file_path}\n')

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
    except:
        print('(ERROR)')
        get_image_error_file_name = f'{PATH_ERRORS}/errors(getImage).txt'
        with open(get_image_error_file_name,'a+') as file:
            file.write(f'{file_name} image not found\n')

def getAllArts(files_names):
    global PATH_IMAGES
    createDir()
    for index, file_name in enumerate(files_names):
        image_file_name = f'{file_name}.jpg'
        if image_file_name in listdir(PATH_IMAGES): # prevent re-downloading of images with same names
            continue
        print(f'{index+1}) {file_name}', end=' ')
        downloadImage(file_name)
            
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
    except:
        error = f'Failed to write {count_file_name}\nGive write permissions'
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
    except:
        set_lyrics_error_file_name = f'{PATH_ERRORS}/errors(setLyrics).txt'
        with open(set_lyrics_error_file_name,'a+') as file:
            file.write(f'Error setting lyrics of {music_file_path}\n')

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
    elements_a = soup.find_all('a', class_='ac-algo')
    
    for element in elements_a:
        href = element['href']
        if azlyrics in href:
            referrer = getYahooReferrerLink(href)
            soup = getParseableSoup(referrer)
            try:
                divs = soup.find_all('div', class_='text-center')[3]
                lyrics = divs.find_all('div')[5].text.strip()
                writelyrics(file_name,lyrics)
            except:
                print('(IP Blocked by https://www.azlyrics.com)')
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
