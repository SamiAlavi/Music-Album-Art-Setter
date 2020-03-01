import os
from combined import getAllArts, setArtRunner, setAlbum

path='Music/'
files = os.listdir(path)    
audioforms = ['.mp3'] #.mp3 supported

if __name__ == '__main__':
    getAllArts(files,audioforms) #getAllArts called
    setArtRunner(path,files,audioforms) #setArtRunner called
    setAlbum(path,files,audioforms) #setAlbum called
