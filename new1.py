import requests
from bs4 import BeautifulSoup
from stagger import read_tag
from os import listdir
from eyed3 import load

def checkformat(query, formats):
    return query.lower().endswith(formats)

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
        for formats in audioforms:
            if checkformat(filename, formats):
                setArt(path+filename,f'downloads/images/{filename}.jpg')
                break

#------------------GET ALBUM ART ------------------#
def saveImage(iname,link):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    img_data = requests.get(link, headers=headers).content
    with open(f'downloads/images/{iname}.jpg', 'wb') as f:
        f.write(img_data)

def downloadImage(url,query):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    try:
        q=query[:-4].replace('&','').replace(' ','+')+' album&size=large'
        soup = requests.get(url+q, headers=headers).content
        soup = BeautifulSoup(r, "html.parser")
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
        for formats in audioforms:
            if checkformat(query, formats):
                print(f'{i+1}) {query}')
                downloadImage(url,query)
                break
            
#------------------ ALBUM NUMBER ------------------#            
def setAlbum(path,music,audioforms):
    with open("#COUNT.txt", "r") as f:
        count=int(f.read())
    
    for i in music:
        for formats in audioforms:
            if checkformat(i, formats):
                count+=1
                mp3=read_tag(path+i)
                mp3.album=str(count)
                mp3.write()
                break
        
    with open("#COUNT.txt", "w") as f:
        f.write(str(count))

#----------------- SET LYRICS ------------------#
def setLyrics(song, fname):
    try:
        with open(fname,'r') as f:
            lyrics = f.read()
        mp3=load(song)
        tagg = mp3.tag
        tagg.lyrics.set(lyrics)
        tagg.save(song)
    except:
        with open('downloads/errors(setLyrics).txt','a+') as f:
            f.write(f'{song} not found in downloads/lyrics\n')

def setLyricsRunner(path,files,audioforms):
    for filename in files:
        for formats in audioforms:
            if checkformat(filename, formats):
                setLyrics(path+filename,f'downloads/lyrics/{filename}.txt')
                break
    
#------------------GET LYRICS ------------------#
def writelyrics(song,lyrics):
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        with open(f'downloads/lyrics/{song}.txt','w', encoding='utf-8') as f:
            f.write(lyrics)

def downloadLyrics(url,song):
    flag = True
    geniuss = 'genius'
    azlyricss = 'azlyrics.com/lyrics'
    
    q = song[:-4].replace(' ','+').replace('&','%26')+' lyrics'
    driver.get(url+q)

    elems = driver.find_elements_by_css_selector('a.result-title')
    for elem in elems:
        link = elem.get_attribute("href")
        if geniuss in link:
            driver.get(link)
            try:
                elem = driver.find_element_by_css_selector('div.jgQsqn')
            except:
                xpath = '/html/body/routable-page/ng-outlet/song-page/div/div/div[2]/div[1]/div/defer-compile[1]/lyrics/div/div/section/p'
                elem = driver.find_element_by_xpath(xpath)
            writelyrics(song,elem.text)
            flag = False
            break
        elif azlyricss in link:
            driver.get(link)
            elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div[5]')
            writelyrics(song,elem.text)
            flag = False
            break
    if flag:
        with open('downloads/errors(getLyrics).txt', 'a', encoding='utf-8') as f:
            f.write(song+'\n')

def getAllLyrics(files,audioforms):
    azlyricss = 'azlyrics.com/lyrics'
    geniuss = 'genius'
    url='https://www.ecosia.org/search?q='

    for i in range(len(files)):
        query = files[i]
        if query+'.txt' in listdir('downloads/lyrics/'):
            continue
        for formats in audioforms:
            if checkformat(query, formats):
                print(f'{i+1}) {query}')
                downloadLyrics(driver,url,query)
                break
