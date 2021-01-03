import os
from new1 import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner, setAlbum

def checkformat(query, formats):
    return query.lower().endswith(formats)

if __name__ == '__main__':    
    os.chdir('src/')
    path='Music/'
    files = os.listdir(path)    
    audioforms = ['.mp3'] #.mp3 supported
    options = ['n','y']

    files = [filename for filename in files for format in audioforms if checkformat(filename, format)]

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
        
    print('\nTotal files:',len(files))
    
    if flag1=='y':
        print('\nGetting album arts')
        getAllArts(files,audioforms) #getAllArts called
        setArtRunner(path,files,audioforms) #setArtRunner called
    
    if flag2=='y':
        print('\nGetting lyrics')
        getAllLyrics(files,audioforms) #getAllLyrics called
        setLyricsRunner(path,files,audioforms) #setLyricsRunner called

    if flag3=='y':
        print('\nGetting album names')
        setAlbum(path,files,audioforms) #setAlbum called
