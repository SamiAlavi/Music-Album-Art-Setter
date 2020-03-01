import os
import stagger

home='Music/'
music=os.listdir(home)

count=-1
    
for i in music:
    if i.endswith('.mp3'):
        count+=1
        mp3=stagger.read_tag(home+i)
        mp3.album=str(count)
        mp3.write()
        print(i)
    
with open("##COUNT.txt", "w") as f:
    f.write(str(count))
