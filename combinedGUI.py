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

def album_names_runner(files_names):
    from src.album_name import start_album_names_runner
    update_callback = lambda error: messagebox.showinfo('Error', error, icon="warning")
    start_album_names_runner(files_names, update_callback)