# Music-Album-Art-Setter
Music metadata editor which automatically sets album covers, album names and lyrics for the given mp3 files

Powered by 
<a href="https://www.bing.com/" target="_blank">
  <img title="Microsoft Bing" alt="Microsoft Bing" width="150" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Microsoft_Bing_logo.svg/220px-Microsoft_Bing_logo.svg.png"/>
</a>
, 
<a href="https://www.yahoo.com/" target="_blank">
  <img title="Yahoo" alt="Yahoo" width="100" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Yahoo%21_%282019%29.svg/220px-Yahoo%21_%282019%29.svg.png"/>
</a>
, 
<a href="https://www.azlyrics.com/" target="_blank">
  <img title="AZLyrics" alt="AZLyrics" width="30" src="https://www.azlyrics.com/az_logo_tr.png"/>
</a>

## Instructions
### For Python Script
1) Make sure you have python and pip installed (https://www.python.org/)
2) Clone this repository
3) Run `pip install -r requirements.txt`
4) Copy your music in the `./Music` directory
5) Run `main.py`

### For Python GUI
1) Download `music_setter.exe` from [Releases(v1.0.0)](https://github.com/SamiAlavi/Music-Album-Art-Setter/releases/tag/v1.0.0 "Releases(v1.0.0)") 
2) Locate your music directory using Browse
3) Check options that you need (album_art, music_lyrics, album_name)
4) Click Run
5) `Album Arts` will be downloaded in `YOUR_MUSIC_DIR/downloads/images/`
6) `Song Lyrics` will be downloaded in `YOUR_MUSIC_DIR/downloads/lyrics/`
7) `Album Names` are currently set using the `count.txt` file
8) `Errors` can be checked from files created in `YOUR_MUSIC_DIR/downloads/`

## Future work
- Get correct `Album Names` from the internet
- Support for other audio formats
- Get `Album Arts`, `Lyrics`, `Album Names` from API instead of Web Scraping
- Use better GUI libraries
- Web Application
    - User enters music name in an input
    - Server sends the album art and lyrics (if available)
- Lyrics with timestamps
    - Get [.lrc](https://en.wikipedia.org/wiki/LRC_(file_format)) files
    - Get timestamps for lyrics using API
    - Match lyrics' lines with song using AI and get the timestamp
- Migration
    - Convert from `Python3` to `Node.js` to support Dynamic Javascript Websites using [Nightmare](https://github.com/segmentio/nightmare)
