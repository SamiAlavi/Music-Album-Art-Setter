from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
########################################################################
import os
from combinedGUI import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner
from combinedGUI import setPaths, setAlbum
########################################################################

def checkformat(query, format):
    return query.lower().endswith(format)

class GUI:
    def toggle(self):
        if self.t_btn.config('text')[-1] == 'True':
            self.t_btn.config(text='False')
        else:
            self.t_btn.config(text='True')

    def getFiles(self):
        self.files = [filename for filename in os.listdir(self.PATH_MUSIC) for format in self.audioforms if checkformat(filename, format)]
        return len(self.files)

    def browseButton(self):
        self.PATH_MUSIC =  filedialog.askdirectory()
        if self.PATH_MUSIC:
            self.changeLabel()
        else:
            self.files = list()
            
    def changeLabel(self):
        t=''
        self.label1.configure(text=f"Path: {self.PATH_MUSIC}")
        length = self.getFiles()
        if length:
            setPaths(self.PATH_MUSIC)
            for i in range(length):
                t+=f"\n{i+1}) {self.files[i]}"
            self.button2.configure(state=NORMAL,fg='white', bg='blue')
        else:
            t = 'No music files found'
            self.button2.configure(state=DISABLED, bg='black')
        self.label2.configure(text=t)
        root.after(1000, self.changeLabel)

    def setupFlags(self):
        self.flag1, self.flag2, self.flag3 = IntVar(),IntVar(),IntVar()
        c1 = Checkbutton(self.frame1, text="Find album arts?", variable=self.flag1, onvalue=1, offvalue=0)
        c2 = Checkbutton(self.frame1, text="Find music lyrics?", variable=self.flag2, onvalue=1, offvalue=0)
        c3 = Checkbutton(self.frame1, text="Rename album names?", variable=self.flag3, onvalue=1, offvalue=0)
        c1.pack(anchor = W)
        c2.pack(anchor = W)
        c3.pack(anchor = W)
    
    def runCombined(self, event=None):
        if not len(self.files):
            return
        # options
        options = self.flag1.get() or self.flag2.get() or self.flag3.get()
        if not options:    
            messagebox.showinfo('', "No option selected")
            
        if self.flag1.get():
            #messagebox.showinfo('', 'Getting album arts') 
            getAllArts(self.files) #getAllArts called
            setArtRunner(self.files) #setArtRunner called  
        
        if self.flag2.get():
            #messagebox.showinfo('', 'Getting lyrics')   
            getAllLyrics(self.files) #getAllLyrics called
            setLyricsRunner(self.files) #setLyricsRunner called

        if self.flag3.get():      
            #messagebox.showinfo('', 'Getting album names')      
            setAlbum(self.files) #setAlbum called
     
        #messagebox.showinfo('', 'Completed')
        
    def __init__(self):
        if 'src' in os.listdir():
            os.chdir('src')      
        
        self.audioforms = ['.mp3'] #.mp3 supported
        self.frame1=Frame(root)
        
        self.button1 = Button(self.frame1,text="Browse Music",height=2,
                              command = self.browseButton)
        self.button1.pack(fill=X)
        self.label1 = Label(self.frame1,text=f"Path: ",height=2,
                            fg='red')
        self.label1.pack(fill=X)
        
        self.setupFlags()
        
        self.label2 = Label(self.frame1, justify=LEFT)
        self.button2 = Button(self.frame1,text="Run",height=2,
                              bg='black',state=DISABLED, command=self.runCombined)
        
        self.button2.pack(fill=X, side=BOTTOM)
        self.label2.pack(fill=BOTH, expand=True, side=BOTTOM)
        self.frame1.pack(fill=BOTH, expand=True)

        self.browseButton()

        # setting for calling function when pressed RETURN
        root.lift()
        root.focus_force()
        root.bind("<Return>", self.runCombined)

root = Tk()      
gui=GUI()
root.mainloop()
