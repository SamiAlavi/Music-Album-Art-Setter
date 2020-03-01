import os
import stagger

home='Music/'
music=os.listdir(home)

print(len(music))
   
with open("##COUNT.txt", "r") as f:
    count=int(f.read())
    
for i in music:
    count+=1
    mp3=stagger.read_tag(home+i)
    mp3.album=str(count)
    mp3.write()
    print(i)
    
with open("##COUNT.txt", "w") as f:
    f.write(str(count))
