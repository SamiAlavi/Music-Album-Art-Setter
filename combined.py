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
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
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
    hideUnhideDir('HIDE')

def hideUnhideDir(command):
    global PATH_ERRORS
    if command=='HIDE':
        call(["attrib", "+H", PATH_ERRORS])
    elif command=='UNHIDE':
        call(["attrib", "-H", PATH_ERRORS])        

def setPaths(path):
    global PATH_MUSIC, PATH_IMAGES, PATH_LYRICS, PATH_ERRORS
    PATH_MUSIC = path
    PATH_ERRORS = f'{path}/downloads'   
    PATH_IMAGES = f'{path}/downloads/images'
    PATH_LYRICS = f'{path}/downloads/lyrics'

#------------------SET ALBUM ART ------------------#
def setArt(songPath, image):
    global PATH_ERRORS
    try:
        mp3=read_tag(songPath)
        mp3.picture=image
        mp3.write()
    except:
        with open(f'{PATH_ERRORS}/errors(setArt).txt','a+') as f:
            f.write(f'Error setting image of {songPath}\n')

def setArtRunner(files):
    global PATH_MUSIC, PATH_IMAGES
    for fname in files:
        setArt(f'{PATH_MUSIC}/{fname}',f'{PATH_IMAGES}/{fname}.jpg')
    hideUnhideDir('UNHIDE')


#------------------GET ALBUM ART ------------------#
def saveImage(fname, url):
    global PATH_IMAGES
    img_data = getUrlContent(url)
    with open(f'{PATH_IMAGES}/{fname}.jpg', 'wb') as f:
        f.write(img_data)

def downloadImage(fname):
    global PATH_ERRORS
    url = 'https://www.bing.com/images/search?q={}&first=1&tsc=ImageBasicHover'
    try:
        param = fname[:-4]
        soup = getParseableSoup(url, param)
        details = soup.find('a', class_='iusc')['m']
        urlImg = loads(details)['murl']
        saveImage(fname, urlImg)
        print()
    except:
        print('(ERROR)')
        with open(f'{PATH_ERRORS}/errors(getImage).txt','a+') as f:
            f.write(fname+' image not found\n')

def getAllArts(files):
    global PATH_IMAGES
    createDir()
    for i, fname in enumerate(files):
        if fname+'.jpg' in listdir(f'{PATH_IMAGES}/'):
            continue
        print(f'{i+1}) {fname}', end=' ')
        downloadImage(fname)
            
#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files):
    global PATH_MUSIC
    fnameCount = 'count.txt'
    try:
        with open(fnameCount, 'r') as f:
            count=int(f.read())
    except:
        count=0
    
    for i, fname in enumerate(files):
        count+=1
        mp3=read_tag(f'{PATH_MUSIC}/{fname}')
        mp3.album=str(count)
        mp3.write()
        
    try:
        with open(fnameCount, 'w') as f:
            f.write(str(count))
    except:
        error = 'Failed to write count.txt\nGive write permissions'
        print(error)

#----------------- SET LYRICS ------------------#
def setLyrics(songPath, fname):
    global PATH_ERRORS
    try:
        with open(fname,'r', encoding='utf-8') as f:
            lyrics = f.read()
        mp3 = load(songPath)
        tagg = mp3.tag
        tagg.lyrics.set(lyrics)
        tagg.save(songPath)
    except:
        with open(f'{PATH_ERRORS}/errors(setLyrics).txt','a+') as f:
            f.write(f'Error setting lyrics of {songPath}\n')

def setLyricsRunner(files):
    global PATH_MUSIC, PATH_LYRICS
    for fname in files:
        setLyrics(f'{PATH_MUSIC}/{fname}',f'{PATH_LYRICS}/{fname}.txt')
    hideUnhideDir('UNHIDE')
    
#------------------GET LYRICS ------------------#
def writelyrics(song, lyrics):
    global PATH_LYRICS
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        with open(f'{PATH_LYRICS}/{song}.txt','w', encoding='utf-8') as f:
            f.write(lyrics)

def getYahooReferrerLink(link):
    soup = getParseableSoup(link)
    metaContent = soup.find_all('meta')[-1]['content'] # yahoo uses redirecting
    referrer = metaContent[7:-1]
    return referrer

def downloadLyrics(fname):
    global PATH_ERRORS
    url='https://search.yahoo.com/search?p={}%20lyrics'
    azlyrics = 'azlyrics.com%2flyrics' # azlyrics temporary blocks IP address
    letssingit = 'letssingit.com%2f'
    lyricsbox = 'lyricsbox.com%2f'
    nott = '%2flyrics'
    
    param = fname[:-4]
    soup = getParseableSoup(url, param)
    elems = soup.find_all('a', class_='ac-algo')
    
    for elem in elems:
        link = elem['href']
        if azlyrics in link:
            referrer = getYahooReferrerLink(link)
            soup = getParseableSoup(referrer)
            try:
                divs = soup.find_all('div', class_='text-center')[3]
                lyrics = divs.find_all('div')[5].text.strip()
                writelyrics(fname,lyrics)
            except:
                print('(IP Blocked by https://www.azlyrics.com)')
            print()
            return
        elif (letssingit in link or lyricsbox in link) and link[-7:]!=nott:
            referrer = getYahooReferrerLink(link)
            soup = getParseableSoup(referrer)
            lyrics = soup.find("div", {"id": "lyrics"}).text.strip()
            writelyrics(fname,lyrics)
            print()
            return
    
    print('(ERROR)')
    with open(f'{PATH_ERRORS}/errors(getLyrics).txt', 'a', encoding='utf-8') as f:
        f.write(fname+' lyrics not found\n')

def getAllLyrics(files):
    global PATH_LYRICS
    createDir()
    for i, fname in enumerate(files):
        if fname+'.txt' in listdir(f'{PATH_LYRICS}/'):
            continue
        print(f'{i+1}) {fname}', end=' ')
        downloadLyrics(fname)
