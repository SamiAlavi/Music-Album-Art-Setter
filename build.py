import sys
import PyInstaller.__main__
from src.helper.helper_gui import APP_ICON, PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_OSX, EXTENSION_XBM, EXTENSION_ICO

def get_icon_path(icon_name):
    extension = EXTENSION_ICO
    if sys.platform == PLATFORM_LINUX or sys.platform == PLATFORM_OSX:
        extension = EXTENSION_XBM
    elif sys.platform == PLATFORM_WINDOWS:
        extension = EXTENSION_ICO
    return f'{icon_name}.{extension}'

icon_path = get_icon_path(APP_ICON)
distribution_name = 'GUI'
script_name = 'GUI.py'

PyInstaller.__main__.run([
    '--add-data',
    f'{icon_path};.',
    '--windowed',
    '--clean',
    '--noconfirm',
    f'--icon={icon_path}',
    f'--name={distribution_name}',
    f'{script_name}',
])
