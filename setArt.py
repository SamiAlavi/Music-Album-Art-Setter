import os
import stagger

path='Music/'
music=os.listdir(path)

def setArt(song, art):
    mp3=stagger.read_tag(song)
    mp3.picture=art
    mp3.write()
    
for i in music:
    if i.endswith('.mp3'):
        try:
            setArt(path+i,'downloads/'+i+'.jpg')
            print(i)
        except:
            with open('errors(setArt).txt','a+') as f:
                f.write('downloads/'+i+'.jpg not found\n')
