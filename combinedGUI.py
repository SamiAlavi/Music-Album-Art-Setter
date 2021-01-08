from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
########################################################################
import requests
from bs4 import BeautifulSoup
from stagger import read_tag
from os import listdir
from eyed3 import load
import os
from time import sleep
########################################################################

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
PATH_MUSIC = None
PATH_IMAGES = None
PATH_LYRICS = None
PATH_ERRORS = None
root = None
progress = None
label1 = None
value = None

def createDir(paths):
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

def setPaths(path):
    global PATH_MUSIC, PATH_IMAGES, PATH_LYRICS, PATH_ERRORS
    PATH_MUSIC = path
    PATH_ERRORS = f'{path}/downloads'
    PATH_IMAGES = f'{path}/downloads/images'
    PATH_LYRICS = f'{path}/downloads/lyrics'
    createDir([PATH_ERRORS, PATH_IMAGES, PATH_LYRICS])

def changeProgress(percentage,file):
    global root, progress, label1, value
    val = percentage*100
    progress['value'] = val
    label1.configure(text=file)
    value.configure(text=f'{round(val,2)}%')
    root.update()

def open_dialog(text):
    global root, progress, label1, value
    root = Tk()
    root.title('Info')
    root.geometry('500x100')
    Label(root,text=text,height=2, fg='red').pack(padx=10)
    label1 = Label(root,text='',height=2)
    progress = Progressbar(root, orient=HORIZONTAL, 
              length=400,maximum=100, mode='determinate')
    value = Label(root,text='',height=2)
    
    label1.pack(expand=True)
    progress.pack(expand=True, side=LEFT)
    value.pack(side=LEFT,expand=True)
    root.update()

#------------------SET ALBUM ART ------------------#
    
def setArt(song, art):
    global PATH_IMAGES, PATH_ERRORS
    try:
        mp3=read_tag(song)
        mp3.picture=art
        mp3.write()
    except:
        with open(f'{PATH_ERRORS}/errors(setArt).txt','a+') as f:
            f.write(f'{song} not found in {PATH_IMAGES}\n')

def setArtRunner(files):
    global PATH_MUSIC, PATH_IMAGES
    for filename in files:
        setArt(f'{PATH_MUSIC}/{filename}',f'{PATH_IMAGES}/{filename}.jpg')

#------------------GET ALBUM ART ------------------#
def saveImage(sname, link):
    global headers, PATH_IMAGES
    img_data = requests.get(link, headers=headers).content
    with open(f'{PATH_IMAGES}/{sname}.jpg', 'wb') as f:
        f.write(img_data)

def downloadImage(url, query):
    global headers, PATH_ERRORS
    try:
        q=query[:-4].replace('&','').replace(' ','+')+' album&size=large'
        soup = requests.get(url+q, headers=headers).content
        soup = BeautifulSoup(soup, "html.parser")
        link = soup.find('a', class_='image-result__link')['href']
        saveImage(query,link)
        print()
    except:
        print('(ERROR)')
        with open(f'{PATH_ERRORS}/errors(downloadImage).txt','a+') as f:
            f.write(query+' not found\n')

def getAllArts(files):
    global PATH_IMAGES
    length = len(files)
    open_dialog('Getting album arts')
    url='https://www.ecosia.org/images?q='
    for i in range(length):
        query = files[i]
        changeProgress((i+1)/length,files[i])
        #sleep(1)
        if query+'.jpg' in listdir(f'{PATH_IMAGES}/'):
            continue
        print(f'{i+1}) {query}', end=' ')
        downloadImage(url,query)
    root.destroy()
            
#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files):
    global PATH_MUSIC
    with open("#COUNT.txt", "r") as f:
        count=int(f.read())
    
    for filename in files:
        count+=1
        mp3=read_tag(f'{PATH_MUSIC}/{filename}')
        mp3.album=str(count)
        mp3.write()
        
    with open("#COUNT.txt", "w") as f:
        f.write(str(count))

#----------------- SET LYRICS ------------------#
def setLyrics(song, fname):
    global PATH_LYRICS, PATH_ERRORS
    try:
        with open(fname,'r', encoding='utf-8') as f:
            lyrics = f.read()
        mp3 = load(song)
        tagg = mp3.tag
        tagg.lyrics.set(lyrics)
        tagg.save(song)
    except:
        with open(f'{PATH_ERRORS}/errors(setLyrics).txt','a+') as f:
            f.write(f'{song} not found in {PATH_LYRICS}\n')

def setLyricsRunner(files):
    global PATH_MUSIC, PATH_LYRICS
    for filename in files:
        setLyrics(f'{PATH_MUSIC}/{filename}',f'{PATH_LYRICS}/{filename}.txt')
    
#------------------GET LYRICS ------------------#
def writelyrics(song, lyrics):
    global PATH_LYRICS
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        with open(f'{PATH_LYRICS}/{song}.txt','w', encoding='utf-8') as f:
            f.write(lyrics)

def downloadLyrics(url, query):
    global headers, PATH_ERRORS
    flag = True
    azlyricss = 'azlyrics.com/lyrics'
    letssingit = 'letssingit.com/'
    lyricsbox = 'lyricsbox.com/'
    nott = '/lyrics'
    
    q = query[:-4].replace(' ','+').replace('&','%26')+'+lyrics'
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
            writelyrics(query,lyrics)
            flag = False
            print()
            break
        elif (letssingit in link or lyricsbox in link) and link[-7:]!=nott:
            soup = requests.get(link, headers=headers).content
            soup = BeautifulSoup(soup, "html.parser")
            lyrics = soup.find("div", {"id": "lyrics"}).text.strip()
            writelyrics(query,lyrics)
            flag = False
            print()
            break
    if flag:
        print('(ERROR)')
        with open(f'{PATH_ERRORS}/errors(getLyrics).txt', 'a', encoding='utf-8') as f:
            f.write(query+'\n')

def getAllLyrics(files):
    global PATH_LYRICS
    length = len(files)
    open_dialog('Getting lyrics')   
    url='https://www.ecosia.org/search?q='
    for i in range(length):
        query = files[i]
        changeProgress((i+1)/length,files[i])
        #sleep(1)
        if query+'.txt' in listdir(f'{PATH_LYRICS}/'):
            continue
        print(f'{i+1}) {query}', end=' ')
        downloadLyrics(url,query)
    root.destroy()
