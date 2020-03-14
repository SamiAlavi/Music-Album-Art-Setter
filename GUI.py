from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Progressbar
from shutil import copy2
from time import sleep
########################################################################
import os
from combined import setArt, setArtRunner, saveImage, downloadImage
from combined import checkformat, getAllArts, setAlbum
########################################################################

root = Tk()

class GUI:
    def browseButton(self):
        files =  filedialog.askopenfilenames(title = "Select file",filetypes = (("mp3 files","*.mp3"),))
        if len(files):
            self.copy(root.tk.splitlist(files),self.path)
            self.changeLabel()

    def browseDriver(self):
        files =  filedialog.askopenfilename(title = "Select file",filetypes = (("exe files","*.exe"),))
        if len(files):
            self.copy([files],os.getcwd()+'/')

    def copy(self,files,path):
        for file in files:
            copy2(file,path+os.path.split(file)[1])
            
    def changeLabel(self):
        t=''
        self.files = os.listdir(self.path) 
        for i in range(1,len(self.files)):
            t+='\n'+self.files[i]
        self.label2.configure(text=t)
        root.after(1000, self.changeLabel)
        
    def changeLB(self): 
        self.flag = 'chromedriver.exe' in os.listdir()
        if self.flag:
            self.label1.configure(text='chromedriver.exe found',
                           foreground="white",background="green")
            self.button1.configure(text="Browse Music", command=lambda: self.browseButton())
            self.button2.configure(state=NORMAL, command=lambda: self.runCombined())
        else:
            self.label1.configure(text='chromedriver.exe not found',
                           foreground="red",background="black")
            self.button1.configure(text="Browse Driver", command=lambda: self.browseDriver())
            self.button2.configure(state=DISABLED)
        root.after(1000, self.changeLB) #it'll call itself continuously       

    def runCombined(self):
        self.button2.configure(state=DISABLED)
        label = Label(master=self.frame1,text='Getting all album arts')
        progress = Progressbar(master=self.frame1, orient = HORIZONTAL, 
              length = 100, mode = 'determinate')
        label.pack(fill=X,side = TOP)
        progress.pack(fill=X,side = TOP)
        
        progress['value'] = 10
        root.update_idletasks()
        
        getAllArts(self.files,self.audioforms) #getAllArts called
        progress['value'] = 50
        label['text']='Setting all album arts'
        root.update_idletasks() 
        

        setArtRunner(self.path,self.files,self.audioforms) #setArtRunner called
        progress['value'] = 75
        label['text']='Setting album numbers'
        root.update_idletasks()
        
        setAlbum(self.path,self.files,self.audioforms) #setAlbum called
        progress['value'] = 100
        root.update_idletasks()         

        label.destroy()
        progress.destroy()
    
    def __init__(self):
        self.flag=False
        
        self.label1 = Label(master=root,height=2)
        self.label1.pack(fill=X)
        self.button1 = Button(master=root,text="Browse",height=2)
        self.button1.pack(fill=X)

        self.frame1=Frame(master=root)        
        self.path='Music/'  
        self.audioforms = ['.mp3'] #.mp3 supported
        
        self.label2 = Label(master=self.frame1)
        self.button2 = Button(master=self.frame1,text="Run",height=2,
                              fg='white',bg='blue')
        self.frame1.pack(fill=BOTH, expand=True)
        self.button2.pack(fill=X,side = BOTTOM)
        self.label2.pack(fill=BOTH, expand=True,side = BOTTOM)

        self.changeLB()
        self.changeLabel()
gui=GUI()

mainloop()
