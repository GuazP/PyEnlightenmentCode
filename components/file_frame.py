import tkinter

class FileFrame():
    def __init__(self):
        file_tabs = []
        pass

    def new_file(self):
        pass

    def load_file(self, path):
        pass

    def save_file(self, path):
        pass

    def save_all_files(self):
        pass


class FileContent():
    def __init__(self, frame):
        self.frame = frame
        self.textarea = Text(frame)
        self.scrollbar = Scrollbar(self.textarea)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        self.scrollbar.config(command = self.textarea.yview) 
        self.textarea.config(yscrollcommand = self.scrollbar.set) 
