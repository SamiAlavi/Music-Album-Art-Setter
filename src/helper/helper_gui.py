from platform import platform
import sys
from tkinter import messagebox
from .constants import APP_ICON_DIR, APP_ICON
from .constants import EXTENSION_ICO, EXTENSION_XBM
from .constants import PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_OSX
from .constants import ICON_WARNING
from .helper_path import join_paths, is_file, get_current_absolute_path

def get_music_icon_path():
    prefix = ''
    extension = EXTENSION_ICO # default icon extension currently set as ICO
    platform = sys.platform
    icon_path = join_paths(APP_ICON_DIR, APP_ICON)


    if platform == PLATFORM_LINUX or platform == PLATFORM_OSX:
        prefix = '@' # TCLError bitmap not defined if path not prefixed with @
        extension = EXTENSION_XBM
    elif platform == PLATFORM_WINDOWS:
        extension = EXTENSION_ICO

    absolute_path = f'{resource_path(icon_path)}.{extension}'
    if is_file(absolute_path):
        return f'{prefix}{absolute_path}'

    return None

def resource_path(relative_path):    
    try:       
        base_path = sys._MEIPASS
    except Exception:
        base_path = get_current_absolute_path()
    return join_paths(base_path, relative_path)

def setup_quit_button(root, title, text):
    root.protocol('WM_DELETE_WINDOW', lambda : quitDialog(root, title, text))

def quitDialog(root, title, text):
    if messagebox.askokcancel(title, text, icon=ICON_WARNING):
        root.destroy()

def get_geometry(width, height):
    return f'{width}x{height}'
