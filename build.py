import PyInstaller.__main__

PyInstaller.__main__.run([
    '--onefile',
    'GUI.py',
    '--add-data',
    'music.ico;.',
    '--icon=music.ico',
    '--windowed'
])
