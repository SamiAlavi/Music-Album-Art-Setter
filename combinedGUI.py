from dialog import Dialog
from tkinter import messagebox

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