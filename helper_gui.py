from tkinter import messagebox
import sys
import os

def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def setupQuit(root, title, text):
    root.protocol('WM_DELETE_WINDOW',
                lambda title=title,text=text : quitDialog(root, title, text))

def quitDialog(root, title, text):
    if messagebox.askokcancel(title, text,icon="warning"):
        root.destroy()