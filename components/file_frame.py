import tkinter
import tkinter.scrolledtext as ScrolledText
import tkinter.scrolledtext as ScrolledText


class FileFrame():
    def __init__(self):
        pass


class FileContent():
    def __init__(self, frame):
        self.frame = frame
        self.textarea = Text(frame)
        self.scrollbar = Scrollbar(self.textarea)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.scrollbar.config(command = self.textarea.yview) 
        self.textarea.config(yscrollcommand = self.scrollbar.set) 
