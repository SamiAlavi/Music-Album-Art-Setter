import os
from new1 import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner, setAlbum

os.chdir('src/')
path='Music/'
files = os.listdir(path)    
audioforms = ['.mp3'] #.mp3 supported
options = ['n','y']

if __name__ == '__main__':
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
        
    print('Total files:',len(files)-1)
    
    if flag1=='y':
        getAllArts(files,audioforms) #getAllArts called
        setArtRunner(path,files,audioforms) #setArtRunner called
    
    if flag2=='y':
        getAllLyrics(files,audioforms) #getAllLyrics called
        setLyricsRunner(path,files,audioforms) #setLyricsRunner called

    if flag3=='y':
        setAlbum(path,files,audioforms) #setAlbum called
