import sys
import shutil
import os
import pyinstaller_versionfile
import PyInstaller.__main__
from src.helper.constants import PLATFORM_WINDOWS, PLATFORM_LINUX, PLATFORM_OSX
from src.helper.constants import APP_ICON_DIR, APP_ICON, EXTENSION_XBM, EXTENSION_ICO
from src.helper.helper import join_paths
from src.helper.helper_path import is_file

def get_music_icon_path():
    extension = EXTENSION_ICO # default icon extension currently set as ICO
    if platform == PLATFORM_LINUX or platform == PLATFORM_OSX:
        extension = EXTENSION_XBM
    elif platform == PLATFORM_WINDOWS:
        extension = EXTENSION_ICO
    return join_paths(APP_ICON_DIR, f'{APP_ICON}.{extension}')

def get_add_data_separator():
    if platform == PLATFORM_LINUX or platform == PLATFORM_OSX:
        return ':'
    elif platform == PLATFORM_WINDOWS:
        return ';'
    return ';'

def create_version_file():
    pyinstaller_versionfile.create_versionfile(
        output_file=version_file_name,
        version=version,
        company_name="",
        file_description="Music metadata editor which automatically sets album covers, album names and lyrics for the given mp3 files",
        internal_name="Music Setter",
        legal_copyright="©",
        original_filename="Music Setter",
        product_name="Music Setter",
        translations=[1033, 1200] # default
    )

def build():
    PyInstaller.__main__.run([
        '--onefile',
        '--add-data',
        f'{icon_path}{add_data_separator}{APP_ICON_DIR}',
        '--windowed',
        '--clean',
        '--noconfirm',
        f'--version-file={version_file_name}',
        f'--icon={icon_path}',
        f'--name={distribution_name}-v{version}-{platform}',
        f'{script_name}',
    ])
    clean_up()

def clean_up():
    print('*** Cleaning Up ***')
    dir_build = 'build'
    
    shutil.rmtree(dir_build, ignore_errors=True)
    os.remove(version_file_name)
    for file_name in os.listdir():
        if file_name.endswith('.spec'):
            os.remove(file_name)


distribution_name = 'music_setter'
script_name = 'GUI.py'
version_file_name = '_version'
version = '1.1.0'

platform = sys.platform
icon_path = get_music_icon_path()
add_data_separator = get_add_data_separator()
create_version_file()
build()
