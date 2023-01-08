import sys
import PyInstaller.__main__
from src.helper.constants import PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_OSX
from src.helper.constants import APP_ICON_DIR, APP_ICON, EXTENSION_XBM, EXTENSION_ICO
from src.helper.helper import join_paths

def get_music_icon_path():
    extension = EXTENSION_ICO # default icon extension currently set as ICO
    if sys.platform == PLATFORM_LINUX or sys.platform == PLATFORM_OSX:
        extension = EXTENSION_XBM
    elif sys.platform == PLATFORM_WINDOWS:
        extension = EXTENSION_ICO
    return join_paths(APP_ICON_DIR, f'{APP_ICON}.{extension}')

def get_add_data_separator():
    if sys.platform == PLATFORM_LINUX or sys.platform == PLATFORM_OSX:
        return ':'
    elif sys.platform == PLATFORM_WINDOWS:
        return ';'
    return ';'

icon_path = get_music_icon_path()
distribution_name = 'GUI'
script_name = 'GUI.py'
add_data_separator = get_add_data_separator()

PyInstaller.__main__.run([
    '--add-data',
    f'{icon_path}{add_data_separator}{APP_ICON_DIR}',
    '--windowed',
    '--clean',
    '--noconfirm',
    f'--icon={icon_path}',
    f'--name={distribution_name}',
    f'{script_name}',
])
