from tkinter import Tk, Label
from tkinter import HORIZONTAL, LEFT
from tkinter.ttk import Progressbar
from ..helper import *
from ..helper.helper_gui import TITLE_INFO, TITLE_APP_QUIT, EMPTY_STR
from ..helper.helper_gui import TEXT_DIALOG_QUIT
from ..helper.helper_gui import COLOR_RED
from ..helper.helper_gui import get_music_icon_path, setup_quit_button

class Dialog():

    def __init__(self, text):
        root = Tk()

        root.iconbitmap(get_music_icon_path())
        root.title(TITLE_INFO)
        width, height = 500, 100
        geometry = f'{width}x{height}'
        root.geometry(geometry)
        root.resizable(0, 0)
        setup_quit_button(root, TITLE_APP_QUIT, TEXT_DIALOG_QUIT)
        
        Label(root, text=text, height=2, fg=COLOR_RED).pack(padx=10)
        self.label1 = Label(root, text=EMPTY_STR, height=2)
        self.progress = Progressbar(root, orient=HORIZONTAL, length=400, maximum=1, mode='determinate')
        self.value = Label(root, text=EMPTY_STR, height=2)
        
        self.label1.pack(expand=True)
        self.progress.pack(expand=True, side=LEFT)
        self.value.pack(side=LEFT, expand=True)

        self.root = root

    def update_progress(self, current, length, file_name):
        self.progress['value'] = current/length
        self.label1.configure(text=file_name)
        self.value.configure(text=f'{current} / {length}')
        self.update()

    def update(self):
        self.root.update()

    def destroy(self):
        self.root.destroy()