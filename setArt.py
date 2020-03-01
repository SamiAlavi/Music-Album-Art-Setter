import os
import stagger

path='Music/'
music=os.listdir(path)

z=0

def setArt(song, art):
    mp3=stagger.read_tag(song)
    mp3.picture=art
    mp3.write()
    
for i in music:    
    z+=1
    try:
        setArt(path+i,'downloads/'+i+'.jpg')
    except:
        with open('errors(setArt).txt','a+') as f:
            f.write(i+'\n')
            print(i)
    if z%50==0:
        print(z)

