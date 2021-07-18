import os
from combined import setupSession, getAllArts, setArtRunner, getAllLyrics, setLyricsRunner, setAlbum, setPaths

def checkformat(query, formats):
    return query.lower().endswith(formats)

if __name__ == '__main__':  
    if 'src' in os.listdir():
        os.chdir('src/')        
        
    PATH_MUSIC='Music'
    setPaths(PATH_MUSIC)
    files = os.listdir(PATH_MUSIC)    
    audioforms = ['.mp3'] #.mp3 supported
    options = ['n','y']

    # options
    flag1 = input('Find album arts? (n/Y) ').lower()
    while flag1 not in options:
        flag1 = input('Find album arts? (n/Y) ').lower()
    
    flag2 = input('Find music lyrics? (N/y) ').lower()
    while flag2 not in options:
        flag2 = input('Find music lyrics? (N/y) ').lower()

    flag3 = input('Rename album names? (N/y) ').lower()
    while flag3 not in options:
        flag3 = input('Rename album names? (N/y) ').lower()
        
    setupSession()
    files = [fname for fname in files for formatt in audioforms if checkformat(fname, formatt)]
    print('\nTotal files:',len(files))
    
    if flag1=='y':
        print('\nGetting album arts')
        getAllArts(files) #getAllArts called
        setArtRunner(files) #setArtRunner called
    
    if flag2=='y':
        print('\nGetting lyrics')
        getAllLyrics(files) #getAllLyrics called
        setLyricsRunner(files) #setLyricsRunner called

    if flag3=='y':
        print('\nGetting album names')
        setAlbum(files) #setAlbum called
