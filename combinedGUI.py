from dialog import Dialog
import requests
from bs4 import BeautifulSoup
from stagger import read_tag
from os import listdir
from eyed3 import load
import os
from subprocess import call
from tkinter import messagebox
import src.helper.helper as helper
from src.helper.helper_path import unhide_directory
#from time import sleep
########################################################################

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#------------------SET ALBUM ART ------------------#
    
def setArt(song, art):
    try:
        mp3=read_tag(song)
        mp3.picture=art
        mp3.write()
    except:
        with open(f'{helper.PATH_ERRORS}/errors(setArt).txt','a+') as f:
            f.write(f'{song} not found in {helper.PATH_IMAGES}\n')

def setArtRunner(files):
    for filename in files:
        setArt(f'{helper.PATH_MUSIC}/{filename}',f'{helper.PATH_IMAGES}/{filename}.jpg')
    unhide_directory(helper.PATH_ERRORS)

def album_arts_runner(files_names):
    from src.album_art import start_album_arts_runner
    dialog = Dialog('Getting album arts')
    start_album_arts_runner(files_names, dialog)
    dialog.destroy()


            
#------------------ ALBUM NUMBER ------------------#            
def setAlbum(files):
    fname = 'count.txt'
    length = len(files)
    dialog = Dialog('Setting album names')
    try:
        with open(fname, 'r') as f:
            count=int(f.read())
    except:
        count=0
    
    for i in range(length):
        dialog.changeProgress(i+1,length,files[i])
        count+=1
        mp3=read_tag(f'{helper.PATH_MUSIC}/{files[i]}')
        mp3.album=str(count)
        mp3.write()
        
    dialog.destroy()
    try:
        with open(fname, 'w') as f:
            f.write(str(count))
    except:
        error = 'Failed to write count.txt\nGive write permissions'        
        messagebox.showinfo('Error',error,icon="warning")

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
        with open(f'{helper.PATH_ERRORS}/errors(setLyrics).txt','a+') as f:
            f.write(f'{song} not found in {helper.PATH_LYRICS}\n')

def setLyricsRunner(files):
    for filename in files:
        setLyrics(f'{helper.PATH_MUSIC}/{filename}',f'{helper.PATH_LYRICS}/{filename}.txt')
    unhide_directory(helper.PATH_ERRORS)
    
#------------------GET LYRICS ------------------#
def writelyrics(song, lyrics):
    if lyrics is not None:
        lyrics = lyrics.replace('’',"'")
        with open(f'{helper.PATH_LYRICS}/{song}.txt','w', encoding='utf-8') as f:
            f.write(lyrics)

def downloadLyrics(url, query):
    global headers
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
            #print()
            break
        elif (letssingit in link or lyricsbox in link) and link[-7:]!=nott:
            soup = requests.get(link, headers=headers).content
            soup = BeautifulSoup(soup, "html.parser")
            lyrics = soup.find("div", {"id": "lyrics"}).text.strip()
            writelyrics(query,lyrics)
            flag = False
            #print()
            break
    if flag:
        #print('(ERROR)')
        with open(f'{helper.PATH_ERRORS}/errors(getLyrics).txt', 'a', encoding='utf-8') as f:
            f.write(query+'\n')

def getAllLyrics(files):
    helper.create_directories()
    length = len(files)
    dialog = Dialog('Getting lyrics')   
    url='https://www.ecosia.org/search?q='
    for i in range(length):
        query = files[i]
        dialog.changeProgress(i+1,length,files[i])
        #sleep(1)
        if query+'.txt' in listdir(f'{helper.PATH_LYRICS}/'):
            continue
        #print(f'{i+1}) {query}', end=' ')
        downloadLyrics(url,query)
    dialog.destroy()
