import os
import stagger

path='Music/'
music=os.listdir(path)
home='downloads/'

z=0

def setArt(song, art):
    mp3=stagger.read_tag(song)
    mp3.picture=art
    mp3.write()
    
for i in music:    
    z+=1
    try:
        a=os.listdir(home+i)
        setArt(path+i,home+i+'/'+a[0])
    except:
        with open('errors(setArt).txt','a+') as f:
            try:
                f.write(i+'\n')
            except:
                print(i)
    if z%50==0:
        print(z)

