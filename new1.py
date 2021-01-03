import requests
from bs4 import BeautifulSoup
from stagger import read_tag
from os import listdir
from eyed3 import load

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    

#------------------SET ALBUM ART ------------------#
def setArt(song, art):
    try:
        mp3=read_tag(song)
        mp3.picture=art
        mp3.write()
    except:
        with open('downloads/errors(setArt).txt','a+') as f:
            f.write(f'{song} not found in downloads/images\n')

def setArtRunner(path,files,audioforms):
    for filename in files:
        setArt(path+filename,f'downloads/images/{filename}.jpg')

#------------------GET ALBUM ART ------------------#
def saveImage(iname,link):
    global headers
    img_data = requests.get(link, headers=headers).content
    with open(f'downloads/images/{iname}.jpg', 'wb') as f:
        f.write(img_data)

def downloadImage(url,query):
    global headers
    try:
        q=query[:-4].replace('&','').replace(' ','+')+' album&size=large'
        soup = requests.get(url+q, headers=headers).content
        soup = BeautifulSoup(soup, "html.parser")
        link = soup.find('a', class_='image-result__link')['href']
        saveImage(query,link)
    except:
        with open('downloads/errors(downloadImage).txt','a+') as f:
            f.write(query+' not found\n')

def getAllArts(search_queries, audioforms):
    url='https://www.ecosia.org/images?q='
    for i in range(len(search_queries)):
        query = search_queries[i]
        if query+'.jpg' in listdir('downloads/images/'):
            continue
        print(f'{i+1}) {query}')
        downloadImage(url,query)
            
#------------------ ALBUM NUMBER ------------------#            
def setAlbum(path,music,audioforms):
    with open("#COUNT.txt", "r") as f:
        count=int(f.read())
    
    for i in music:
        count+=1
        mp3=read_tag(path+i)
        mp3.album=str(count)
        mp3.write()
        
    with open("#COUNT.txt", "w") as f:
        f.write(str(count))

#----------------- SET LYRICS ------------------#
def setLyrics(song, fname):
    try:
        with open(fname,'r', encoding='utf-8') as f:
            lyrics = f.read()
        mp3 = load(song)
        tagg = mp3.tag
        tagg.lyrics.set(lyrics)
        tagg.save(song)
    except:
        with open('downloads/errors(setLyrics).txt','a+') as f:
            f.write(f'{song} not found in downloads/lyrics\n')

def setLyricsRunner(path,files,audioforms):
    for filename in files:
        setLyrics(path+filename,f'downloads/lyrics/{filename}.txt')
    
#------------------GET LYRICS ------------------#
def writelyrics(song,lyrics):
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        with open(f'downloads/lyrics/{song}.txt','w', encoding='utf-8') as f:
            f.write(lyrics)

def downloadLyrics(url,song):
    global headers
    flag = True
    azlyricss = 'azlyrics.com/lyrics'
    letssingit = 'letssingit.com/'
    lyricsbox = 'lyricsbox.com/'
    nott = '/lyrics'
    
    q = song[:-4].replace(' ','+').replace('&','%26')+'+lyrics'
    soup = requests.get(url+q, headers=headers).content
    soup = BeautifulSoup(soup, "html.parser")
    elems = soup.find_all('a', class_='result-url js-result-url')
    
    for elem in elems:
        link = elem['href']
        if azlyricss in link:
            soup = requests.get(link, headers=headers).content
            soup = BeautifulSoup(soup, "html.parser")
            divs = soup.find_all('div', class_='text-center')[3]
            lyrics = divs.find_all('div')[5].text.strip()
            writelyrics(song,lyrics)
            flag = False
            break
        elif (letssingit in link or lyricsbox in link) and link[-7:]!=nott:
            soup = requests.get(link, headers=headers).content
            soup = BeautifulSoup(soup, "html.parser")
            lyrics = soup.find("div", {"id": "lyrics"}).text.strip()
            writelyrics(song,lyrics)
            flag = False
            break
    if flag:
        with open('downloads/errors(getLyrics).txt', 'a', encoding='utf-8') as f:
            f.write(song+'\n')

def getAllLyrics(files,audioforms):
    url='https://www.ecosia.org/search?q='
    for i in range(len(files)):
        query = files[i]
        if query+'.txt' in listdir('downloads/lyrics/'):
            continue
        print(f'{i+1}) {query}')
        downloadLyrics(url,query)
