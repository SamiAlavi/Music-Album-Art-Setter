import PyInstaller.__main__

PyInstaller.__main__.run([
    '--add-data',
    'music.ico;.',
    '--windowed',
    '--clean',
    '--icon=music.ico',
    '--name=GUI',
    'GUI.py',
])
