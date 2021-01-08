# Music-Album-Art-Setter
Music metadata editor which automatically sets album covers, album names and lyrics for the given mp3 files

---
# Instructions
### For Script
1) Make sure you have python and pip installed (https://www.python.org/)
2) Clone this repository
3) Run `pip install -r requirements.txt`
4) Copy your music in the `./Music` directory
5) Run `main.py`

## For GUI
1) Download `music_setter.exe` from 
2) Locate your music directory using Browse
3) Check options that you need (album_art, music_lyrics, album_name)
4) Click Run
5) `Album Arts` will be downloaded in `YOUR_MUSIC_DIR/downloads/images/`
6) `Song Lyrics` will be downloaded in `YOUR_MUSIC_DIR/downloads/lyrics/`
7) `Album Names` are currently set using the `.count` file
8) `Errors` can be checked from files created in `YOUR_MUSIC_DIR/downloads/`

---
# Future work
- Get correct `Album Names` from the internet
- Support for other audio formats
