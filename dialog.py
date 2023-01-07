from tkinter import Tk, Label
from tkinter import HORIZONTAL, LEFT
from tkinter.ttk import Progressbar
from helper_gui import resource_path, setupQuit

class Dialog():

    def __init__(self, text):
        root = Tk()

        #global root, progress, label1, value
        root.iconbitmap(resource_path('music.ico'))
        root.title('Info')
        root.geometry('500x100')
        root.resizable(0,0)
        setupQuit(root, 'Close?', 'Process is running\nAre you sure you want to close?')
        
        Label(root,text=text,height=2, fg='red').pack(padx=10)
        self.label1 = Label(root,text='',height=2)
        self.progress = Progressbar(root, orient=HORIZONTAL, 
                length=400,maximum=1, mode='determinate')
        self.value = Label(root,text='',height=2)
        
        self.label1.pack(expand=True)
        self.progress.pack(expand=True, side=LEFT)
        self.value.pack(side=LEFT,expand=True)

        self.root = root

    def changeProgress(self, i, length, file):
        self.progress['value'] = i/length
        self.label1.configure(text=file)
        self.value.configure(text=f'{i} / {length}')
        self.update()

    def update(self):
        self.root.update()

    def destroy(self):
        self.root.destroy()
    

if __name__ == "__main__":
    dialog = Dialog("Test Dialog")