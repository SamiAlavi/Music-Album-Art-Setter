# Music-Album-Art-Setter
Music metadata editor which automatically sets album covers, album names and lyrics for the given mp3 files

## Powered by 
- [Microsoft Bing](https://www.bing.com/)
- [Yahoo!](https://search.yahoo.com/)
- [AZLyrics](https://www.azlyrics.com/)
- [LetsSingIt](https://www.letssingit.com/)
- [LyricsBOX](https://www.lyricsbox.com/)

## Releases
- Latest release can be found it on the [Releases](https://github.com/SamiAlavi/Music-Album-Art-Setter/releases) page

## Instructions

### OS Support
- Windows
- Linux

### Installation
1) Make sure you have [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installation/) installed
2) Clone this repository
3) Run `pip install -r requirements.txt`

### For Python Script
1) Copy your music in the `./Music` directory
2) Run `python main.py`

### For Python GUI
1) Run `python GUI.py`
2) Locate your music directory using Browse
3) Check options that you need (album_art, music_lyrics, album_name)
4) Click Run
5) `Album Arts` will be downloaded in `YOUR_MUSIC_DIR/downloads/images/`
6) `Song Lyrics` will be downloaded in `YOUR_MUSIC_DIR/downloads/lyrics/`
7) `Album Names` are currently set using the `count.txt` file
8) `Errors` can be checked from files created in `YOUR_MUSIC_DIR/downloads/`

### Build
- Run `python build.py`

## Future work
- Write unit tests
- Add proxy support
- CI/CD and automation
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
