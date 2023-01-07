from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
########################################################################
from os import listdir
from combinedGUI import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner
from combinedGUI import setPaths, setAlbum, setupQuit, resource_path
########################################################################
from src.helper.helper_path import validate_extension

class GUI:
    previous = None
    EXTENSIONS_SUPPORTED = ['.mp3']
        
    def __init__(self, root):
        self.setup_first_frame()
        self.browseButton()        
        root.bind("<Return>", self.runCombined) # setting for calling function when pressed KEY

    def setup_first_frame(self):
        self.frame1 = Frame(root) # Frame 1
        
        self.button1 = Button(self.frame1,text="Browse Music",height=2,
                              fg='white', bg='blue',
                              command = self.browseButton)
        self.button1.bind("<Enter>", self.on_enter)
        self.button1.bind("<Leave>", self.on_leave)

        self.label1 = Label(self.frame1,text=f"Path: ",height=2,
                            fg='red')
        
        self.button1.pack(fill=X)
        self.label1.pack(fill=X)
        
        self.setup_options()
        
        self.setup_second_frame()

        self.frame1.pack(fill=BOTH)

    def setup_second_frame(self):
        self.frame2=Frame(self.frame1) # Frame 2

        self.listbox = Listbox(self.frame2)
        scrollbar = Scrollbar(self.frame2)
        scrollbar.config(command = self.listbox.yview) 
        self.listbox.config(yscrollcommand = scrollbar.set)
        
        self.button2 = Button(self.frame1,text="Run",height=2,
                              bg='black',state=DISABLED, command=self.runCombined)
        self.button2.bind("<Enter>", self.on_enter)
        self.button2.bind("<Leave>", self.on_leave)

        scrollbar.pack(fill=BOTH, side=RIGHT)
        self.listbox.pack(fill=BOTH, side=BOTTOM)        
        self.button2.pack(fill=BOTH, side=BOTTOM)
        self.frame2.pack(fill=BOTH)
    
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

    def get_files_names(self):
        return [file_name for file_name in listdir(self.PATH_MUSIC) for extension in self.EXTENSIONS_SUPPORTED if validate_extension(file_name, extension)]

    def browseButton(self):
        self.PATH_MUSIC =  filedialog.askdirectory()
        if self.PATH_MUSIC:
            self.changeLabel()
        else:
            self.files_names = list()
            
    def changeLabel(self):
        self.label1.configure(text=f"Path: {self.PATH_MUSIC}")
        self.listbox.delete(0,END)
        self.files_names = self.get_files_names()
        length = len(self.files_names)
        temp1='     '
        if length:
            setPaths(self.PATH_MUSIC)
            for i in range(length):
                t=f"\n{temp1}{i+1}) {self.files_names[i]}"
                self.listbox.insert(END, t) 
            self.button2.configure(state=NORMAL,fg='white', bg='blue')
        else:
            t = 'No music files found'
            self.button2.configure(state=DISABLED, bg='black')
        #root.after(1000, self.changeLabel)

    def setup_options(self):
        self.find_album_arts = IntVar()
        self.find_music_lyrics = IntVar()
        self.rename_albums_names = IntVar()

        c1 = Checkbutton(self.frame1, text="Find album arts?", variable=self.find_album_arts, onvalue=1, offvalue=0)
        c2 = Checkbutton(self.frame1, text="Find music lyrics?", variable=self.find_music_lyrics, onvalue=1, offvalue=0)
        c3 = Checkbutton(self.frame1, text="Rename album names?", variable=self.rename_albums_names, onvalue=1, offvalue=0)
        
        c1.pack(anchor=W, ipadx=10)
        c2.pack(anchor=W, ipadx=10)
        c3.pack(anchor=W, ipadx=10)
    
    def runCombined(self, event=None):
        if not len(self.files_names):
            return
        # options
        options = self.find_album_arts.get() or self.find_music_lyrics.get() or self.rename_albums_names.get()
        if not options:    
            messagebox.showinfo('', "No option selected")
            
        if self.find_album_arts.get(): 
            getAllArts(self.files_names) #getAllArts called
            setArtRunner(self.files_names) #setArtRunner called  
        
        if self.find_music_lyrics.get(): 
            getAllLyrics(self.files_names) #getAllLyrics called
            setLyricsRunner(self.files_names) #setLyricsRunner called

        if self.rename_albums_names.get():           
            setAlbum(self.files_names) #setAlbum called
     
        #messagebox.showinfo('', 'Completed')

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

root = setupRoot()
gui = GUI(root)
root.mainloop()
