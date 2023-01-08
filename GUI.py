
import sys
from tkinter import Tk, Frame, Button, Label, Checkbutton, Listbox, Scrollbar, messagebox, filedialog
from tkinter import IntVar, BOTH, RIGHT, BOTTOM, NORMAL, DISABLED, END, W, X
from src.helper.constants import APP_TITLE, EMPTY_STR
from src.helper.constants import TITLE_APP_QUIT, TITLE_COMPLETED
from src.helper.constants import TEXT_APP_QUIT, TEXT_NO_OPTIONS, TEXT_NO_MUSIC_FILES, TEXT_BROWSE, TEXT_RUN, TEXT_PATH
from src.helper.constants import TEXT_ALBUM_ARTS, TEXT_LYRICS, TEXT_ALBUM_NAMES
from src.helper.constants import EVENT_RETURN, EVENT_ENTER, EVENT_LEAVE
from src.helper.constants import COLOR_WHITE, COLOR_BLUE, COLOR_RED, COLOR_BLACK, COLOR_DARK_BLUE
from src.helper.helper import setPaths, get_music_files_names
from src.helper.helper_gui import get_music_icon_path, setup_quit_button, get_geometry
from src.gui.NullIO import NullIO
from src.gui.combinedGUI import album_arts_runner, lyrics_runner, album_names_runner

class GUI(Tk):
    previous_widget_color = None
        
    def __init__(self):
        super().__init__()

        self.setup_root()
        self.setup_first_frame()
        self.browse_button()        
        self.bind(EVENT_RETURN, self.run_combined)

    def setup_root(self):
        self.iconbitmap(get_music_icon_path())
        self.title(APP_TITLE)
        width, height = 500, 300
        geometry = get_geometry(width, height)
        self.geometry(geometry)
        self.lift()
        self.focus_force()
        setup_quit_button(self, TITLE_APP_QUIT, TEXT_APP_QUIT)

    def setup_first_frame(self):
        self.frame1 = self.get_first_frame()        
        self.setup_options()        
        self.setup_second_frame()
        self.frame1.pack(fill=BOTH)

    def get_first_frame(self):
        frame = Frame(self)
        
        button = Button(frame, text=TEXT_BROWSE, height=2, fg=COLOR_WHITE, bg=COLOR_BLUE, command = self.browse_button)
        button.bind(EVENT_ENTER, self.on_enter)
        button.bind(EVENT_LEAVE, self.on_leave)
        
        text = TEXT_PATH.format(EMPTY_STR)
        self.label1 = Label(frame, text=text, height=2, fg=COLOR_RED)
        
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
        scrollbar.config(command=self.listbox.yview) 
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        self.button2 = Button(self.frame1, text=TEXT_RUN, height=2, bg=COLOR_BLACK, state=DISABLED, command=self.run_combined)
        self.button2.bind(EVENT_ENTER, self.on_enter)
        self.button2.bind(EVENT_LEAVE, self.on_leave)

        scrollbar.pack(fill=BOTH, side=RIGHT)
        self.listbox.pack(fill=BOTH, side=BOTTOM)        
        self.button2.pack(fill=BOTH, side=BOTTOM)

        return frame
    
    def on_enter(self, event):
        self.previous_widget_color = event.widget['background']
        if not self.previous_widget_color==COLOR_BLACK:
            event.widget['background'] = COLOR_DARK_BLUE

    def on_leave(self, event):
        event.widget['background'] = self.previous_widget_color

    def browse_button(self):
        self.PATH_MUSIC =  filedialog.askdirectory()
        if self.PATH_MUSIC:
            self.update_label()
            self.update_files_list()
        else:
            self.files_names = list()
            
    def update_label(self):
        text = TEXT_PATH.format(self.PATH_MUSIC)
        self.label1.configure(text=text)

    def update_files_list(self):
        self.listbox.delete(0, END)
        self.files_names = get_music_files_names(self.PATH_MUSIC)
        padding_left = '     '

        if len(self.files_names):
            setPaths(self.PATH_MUSIC)
            for index, file_name in enumerate(self.files_names):
                text = f"\n{padding_left}{index+1}) {file_name}"
                self.listbox.insert(END, text) 
            self.button2.configure(state=NORMAL, fg=COLOR_WHITE, bg=COLOR_BLUE)
        else:
            #text = TEXT_NO_MUSIC_FILES
            self.button2.configure(state=DISABLED, bg=COLOR_BLACK)

    def setup_options(self):
        self.find_album_arts = IntVar()
        self.find_music_lyrics = IntVar()
        self.rename_albums_names = IntVar()

        checkbox_arts = Checkbutton(self.frame1, text=TEXT_ALBUM_ARTS, variable=self.find_album_arts, onvalue=1, offvalue=0)
        checkbox_lyrics = Checkbutton(self.frame1, text=TEXT_LYRICS, variable=self.find_music_lyrics, onvalue=1, offvalue=0)
        checkbox_name = Checkbutton(self.frame1, text=TEXT_ALBUM_NAMES, variable=self.rename_albums_names, onvalue=1, offvalue=0)

        checkbox_arts.pack(anchor=W, ipadx=10)
        checkbox_lyrics.pack(anchor=W, ipadx=10)
        checkbox_name.pack(anchor=W, ipadx=10)
    
    def run_combined(self, event=None):
        if not len(self.files_names):
            return

        find_album_arts = self.find_album_arts.get()
        find_music_lyrics = self.find_music_lyrics.get()
        rename_albums_names = self.rename_albums_names.get()

        options = find_album_arts or find_music_lyrics or rename_albums_names
        if not options:    
            messagebox.showinfo(EMPTY_STR, TEXT_NO_OPTIONS)
            return
            
        if find_album_arts:
            album_arts_runner(self.files_names)
        
        if find_music_lyrics:
            lyrics_runner(self.files_names)

        if rename_albums_names:
            album_names_runner(self.files_names)
     
        #messagebox.showinfo(EMPTY_STR, TITLE_COMPLETED)

sys.stdout = NullIO()
gui = GUI()
gui.mainloop()
