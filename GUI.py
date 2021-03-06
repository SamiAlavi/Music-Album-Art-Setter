from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
########################################################################
import os
from combinedGUI import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner
from combinedGUI import setPaths, setAlbum, setupQuit, resource_path
########################################################################

def checkformat(query, format):
    return query.lower().endswith(format)

class GUI:
    previous = None
    audioforms = ['.mp3'] #.mp3 supported
    
    def on_enter(self,e):
        self.previous = e.widget['background']
        if not self.previous=='black':
            e.widget['background'] = '#0000b2'
    def on_leave(self,e):
        e.widget['background'] = self.previous
        
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
        self.label1.configure(text=f"Path: {self.PATH_MUSIC}")
        self.listbox.delete(0,END)
        length = self.getFiles()
        temp1='     '
        if length:
            setPaths(self.PATH_MUSIC)
            for i in range(length):
                t=f"\n{temp1}{i+1}) {self.files[i]}"
                self.listbox.insert(END, t) 
            self.button2.configure(state=NORMAL,fg='white', bg='blue')
        else:
            t = 'No music files found'
            self.button2.configure(state=DISABLED, bg='black')
        #root.after(1000, self.changeLabel)

    def setupOptions(self):
        self.flag1, self.flag2, self.flag3 = IntVar(),IntVar(),IntVar()
        c1 = Checkbutton(self.frame1, text="Find album arts?", variable=self.flag1, onvalue=1, offvalue=0)
        c2 = Checkbutton(self.frame1, text="Find music lyrics?", variable=self.flag2, onvalue=1, offvalue=0)
        c3 = Checkbutton(self.frame1, text="Rename album names?", variable=self.flag3, onvalue=1, offvalue=0)
        c1.pack(anchor=W, ipadx=10)
        c2.pack(anchor=W, ipadx=10)
        c3.pack(anchor=W, ipadx=10)
    
    def runCombined(self, event=None):
        if not len(self.files):
            return
        # options
        options = self.flag1.get() or self.flag2.get() or self.flag3.get()
        if not options:    
            messagebox.showinfo('', "No option selected")
            
        if self.flag1.get(): 
            getAllArts(self.files) #getAllArts called
            setArtRunner(self.files) #setArtRunner called  
        
        if self.flag2.get(): 
            getAllLyrics(self.files) #getAllLyrics called
            setLyricsRunner(self.files) #setLyricsRunner called

        if self.flag3.get():           
            setAlbum(self.files) #setAlbum called
     
        #messagebox.showinfo('', 'Completed')
        
    def __init__(self):   
        
        self.frame1=Frame(root) # Frame 1
        
        self.button1 = Button(self.frame1,text="Browse Music",height=2,
                              fg='white', bg='blue',
                              command = self.browseButton)        
        self.label1 = Label(self.frame1,text=f"Path: ",height=2,
                            fg='red')
        self.button2 = Button(self.frame1,text="Run",height=2,
                              bg='black',state=DISABLED, command=self.runCombined)
        
        self.button1.pack(fill=X)
        self.label1.pack(fill=X)
        
        self.setupOptions() # options
        
        self.frame2=Frame(self.frame1) # Frame 2        
        self.listbox = Listbox(self.frame2)
        scrollbar = Scrollbar(self.frame2)
        self.listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.listbox.yview) 

        scrollbar.pack(fill=BOTH, side=RIGHT)
        self.listbox.pack(fill=BOTH, side=BOTTOM)        
        self.button2.pack(fill=BOTH, side=BOTTOM)
        self.frame2.pack(fill=BOTH)
        self.frame1.pack(fill=BOTH)

        self.button1.bind("<Enter>", self.on_enter)
        self.button1.bind("<Leave>", self.on_leave)
        self.button2.bind("<Enter>", self.on_enter)
        self.button2.bind("<Leave>", self.on_leave)

        self.browseButton()
        
        # setting for calling function when pressed KEY
        root.bind("<Return>", self.runCombined)

def setupRoot():
    root = Tk()
    root.iconbitmap(resource_path('music.ico'))
    root.title('Music Album Art Setter')
    root.geometry('500x300')
    root.lift()
    root.focus_force()
    title = 'Quit?'
    text = 'Are you sure you want to quit?'
    setupQuit(root, title, text)
    return root

if 'src' in os.listdir():
    os.chdir('src')

root = setupRoot()
gui=GUI()
root.mainloop()
