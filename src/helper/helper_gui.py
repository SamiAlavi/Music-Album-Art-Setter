import sys
import os
from tkinter import messagebox

APP_TITLE = 'Music Album Art Setter'
APP_ICON_DIR = 'icons'
APP_ICON = 'music'
EMPTY_STR = ''

EVENT_RETURN = '<Return>'
EVENT_ENTER = '<Enter>'
EVENT_LEAVE = '<Leave>'

TITLE_APP_QUIT = 'Quit?'
TITLE_DIALOG_QUIT = 'Close?'
TITLE_ERROR = 'Error'
TITLE_INFO = 'Info'
TITLE_COMPLETED = 'Completed'
TITLE_ALBUM_ARTS = 'Getting album arts'
TITLE_LYRICS = 'Getting lyrics'

TEXT_PATH = 'Path: {}'
TEXT_APP_QUIT = 'Are you sure you want to quit?'
TEXT_DIALOG_QUIT = 'Process is running\nAre you sure you want to close?'
TEXT_NO_OPTIONS = 'No option selected'
TEXT_NO_MUSIC_FILES = 'No music files found'
TEXT_BROWSE = 'Browse Music'
TEXT_RUN = 'Run'
TEXT_ALBUM_ARTS = 'Find album arts?'
TEXT_LYRICS = 'Find music lyrics?'
TEXT_ALBUM_NAMES = 'Rename album names?'

COLOR_BLACK = 'black'
COLOR_DARK_BLUE = '#0000b2'
COLOR_WHITE = 'white'
COLOR_BLUE = 'blue'
COLOR_RED = 'red'

ICON_WARNING = 'warning'

EXTENSION_ICO = 'ico'
EXTENSION_XBM = 'xbm'

PLATFORM_WINDOWS = 'win32'
PLATFORM_LINUX = 'linux'
PLATFORM_OSX = 'darwin'

def get_music_icon_path():
    icon_path = f'{APP_ICON_DIR}/{APP_ICON}'
    absolute_path = resource_path(icon_path)
    if sys.platform == PLATFORM_LINUX or sys.platform == PLATFORM_OSX:
        return f'@{absolute_path}.{EXTENSION_XBM}'
    elif sys.platform == PLATFORM_WINDOWS:
        return f'{absolute_path}.{EXTENSION_ICO}'
    return None

def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def setup_quit_button(root, title, text):
    root.protocol('WM_DELETE_WINDOW', lambda : quitDialog(root, title, text))

def quitDialog(root, title, text):
    if messagebox.askokcancel(title, text, icon=ICON_WARNING):
        root.destroy()