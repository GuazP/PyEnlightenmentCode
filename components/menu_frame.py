import tkinter
from tkinter.messagebox import *
from tkinter.filedialog import *

class MenuBar():
    def __init__(self, _root, MainWindow):
        self._root = _root
        self.menubar = Menu(_root)
        self.filemenu = Menu(_root, tearoff=0) 
        self.editmenu = Menu(_root, tearoff=0) 
        self.helpmenu = Menu(_root, tearoff=0) 
        
        self.filemenu.add_command(label = "New", 
                                  command = MainWindow.new_file) 
        self.filemenu.add_command(label = "Open", 
                                  command = MainWindow.load_file) 
        self.filemenu.add_command(label = "Save", 
                                  command = MainWindow.save_file) 
        self.filemenu.add_command(label = "Save as ...", 
                                  command = lambda: MainWindow.save_file(True)) 
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", 
                                  command = lambda: MainWindow.exit_(self._root)) 
        self.menubar.add_cascade(label = "File", 
                                 menu = self.filemenu) 

        self.editmenu.add_command(label = "Settings",
                                  command = MainWindow.configure_settings)
        self.menubar.add_cascade(label = "Edit", 
                                 menu = self.editmenu) 
          
        self.helpmenu.add_command(label = "About PyEnlightenmentCode", 
                                        command = lambda: None) 
        self.helpmenu.add_cascade(label = "Help", 
                                       menu = lambda: None) 
        self.menubar.add_cascade(label = "About", 
                                 menu = self.helpmenu) 
          
        self._root.config(menu = self.menubar) 
          