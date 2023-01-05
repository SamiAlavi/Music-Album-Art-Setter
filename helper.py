import requests
from bs4 import BeautifulSoup
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

setupSession()