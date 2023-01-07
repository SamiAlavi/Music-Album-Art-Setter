from tkinter import Tk, Frame, Button, Label, Checkbutton, Listbox, Scrollbar, messagebox, filedialog
from tkinter import IntVar, BOTH, RIGHT, BOTTOM, NORMAL, DISABLED, END, W, X
########################################################################
from os import listdir
from combinedGUI import getAllArts, setArtRunner, getAllLyrics, setLyricsRunner, setAlbum
from helper_gui import resource_path, setupQuit
from src.helper.helper import setPaths
########################################################################
from src.helper.helper_path import validate_extension

class GUI(Tk):
    previous_widget_color = None
    EXTENSIONS_SUPPORTED = ['.mp3']
        
    def __init__(self):
        super().__init__()

        self.setup_root()
        self.setup_first_frame()
        self.browse_button()        
        self.bind("<Return>", self.run_combined) # setting for calling function when pressed KEY

    def setup_root(self):
        self.iconbitmap(resource_path('music.ico'))
        self.title('Music Album Art Setter')
        self.geometry('500x300')
        self.lift()
        self.focus_force()
        title = 'Quit?'
        text = 'Are you sure you want to quit?'
        setupQuit(self, title, text)

    def setup_first_frame(self):
        self.frame1 = self.get_first_frame()        
        self.setup_options()        
        self.setup_second_frame()
        self.frame1.pack(fill=BOTH)

    def get_first_frame(self):
        frame = Frame(self)
        
        button = Button(frame,text="Browse Music",height=2,
                              fg='white', bg='blue',
                              command = self.browse_button)
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)

        self.label1 = Label(frame,text=f"Path: ",height=2,
                            fg='red')
        
        button.pack(fill=X)
        self.label1.pack(fill=X)

        return frame

    def setup_second_frame(self):
        self.frame2 = self.get_second_frame()        
        self.frame2.pack(fill=BOTH)

    def get_second_frame(self):
        frame = Frame(self.frame1)

        self.listbox = Listbox(frame)
        scrollbar = Scrollbar(frame)
        scrollbar.config(command = self.listbox.yview) 
        self.listbox.config(yscrollcommand = scrollbar.set)
        
        self.button2 = Button(self.frame1,text="Run",height=2,
                              bg='black',state=DISABLED, command=self.run_combined)
        self.button2.bind("<Enter>", self.on_enter)
        self.button2.bind("<Leave>", self.on_leave)

        scrollbar.pack(fill=BOTH, side=RIGHT)
        self.listbox.pack(fill=BOTH, side=BOTTOM)        
        self.button2.pack(fill=BOTH, side=BOTTOM)

        return frame
    
    def on_enter(self, event):
        self.previous_widget_color = event.widget['background']
        if not self.previous_widget_color=='black':
            event.widget['background'] = '#0000b2'

    def on_leave(self, event):
        event.widget['background'] = self.previous_widget_color

    def get_files_names(self):
        return [file_name for file_name in listdir(self.PATH_MUSIC) for extension in self.EXTENSIONS_SUPPORTED if validate_extension(file_name, extension)]

    def browse_button(self):
        self.PATH_MUSIC =  filedialog.askdirectory()
        if self.PATH_MUSIC:
            self.update_label()
            self.update_files_list()
        else:
            self.files_names = list()
            
    def update_label(self):
        self.label1.configure(text=f"Path: {self.PATH_MUSIC}")
        #root.after(1000, self.changeLabel)

    def update_files_list(self):
        self.listbox.delete(0,END)
        self.files_names = self.get_files_names()
        padding_left = '     '

        if len(self.files_names):
            setPaths(self.PATH_MUSIC)
            for index, file_name in enumerate(self.files_names):
                text = f"\n{padding_left}{index+1}) {file_name}"
                self.listbox.insert(END, text) 
            self.button2.configure(state=NORMAL, fg='white', bg='blue')
        else:
            text = 'No music files found'
            self.button2.configure(state=DISABLED, bg='black')
        #root.after(1000, self.update_files_list)

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
    
    def run_combined(self, event=None):
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

gui = GUI()
gui.mainloop()
