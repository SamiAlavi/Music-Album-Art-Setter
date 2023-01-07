from dialog import Dialog
from tkinter import messagebox
from helper_gui import TITLE_ALBUM_ARTS, TITLE_LYRICS, TITLE_ERROR
from helper_gui import ICON_WARNING

def album_arts_runner(files_names):
    from src.album_art import start_album_arts_runner
    dialog = Dialog(TITLE_ALBUM_ARTS)
    start_album_arts_runner(files_names, dialog)
    dialog.destroy()

def lyrics_runner(files_names):
    from src.lyrics import start_lyrics_runner
    dialog = Dialog(TITLE_LYRICS)
    start_lyrics_runner(files_names, dialog)
    dialog.destroy()

def album_names_runner(files_names):
    from src.album_name import start_album_names_runner
    update_callback = lambda error: messagebox.showinfo(TITLE_ERROR, error, icon=ICON_WARNING)
    start_album_names_runner(files_names, update_callback)