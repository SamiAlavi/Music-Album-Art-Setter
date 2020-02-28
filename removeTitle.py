import os
import eyed3
from eyed3 import id3

home='Music/'
music=os.listdir(home)

print(len(music))

def removeTitle(song):
    audiofile = eyed3.load(song)
     
    if (audiofile.tag == None):
        audiofile.initTag()

    audiofile.tag.title=None
    audiofile.tag.save()

count=-1

for i in music:
    count+=1
    #renaming due to name encoding errors while loading song
    os.rename(home+i, home+'aaa.mp3') 
    if count%100==0:
        print(count)
    try:
        removeTitle(home+'aaa.mp3')
    except:
        print(i)
    os.rename(home+'aaa.mp3',home+i)
    
