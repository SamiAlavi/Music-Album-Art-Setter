from requests import Session
from bs4 import BeautifulSoup
from urllib.parse import quote

SESSION = None

def setupSession():
    global SESSION
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }
    SESSION = Session()
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

setupSession()
