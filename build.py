import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    'src/GUI.py',
    '--add-data',
    'src/music.ico;.',
    '--icon=src/music.ico',
    '--windowed'
])
