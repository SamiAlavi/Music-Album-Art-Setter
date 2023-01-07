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

def album_arts_runner(files_names):
    from src.album_art import start_album_arts_runner
    dialog = Dialog('Getting album arts')
    start_album_arts_runner(files_names, dialog)
    dialog.destroy()

def lyrics_runner(files_names):
    from src.lyrics import start_lyrics_runner
    dialog = Dialog('Getting lyrics')
    start_lyrics_runner(files_names, dialog)
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
