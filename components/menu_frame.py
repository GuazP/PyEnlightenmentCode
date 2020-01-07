import tkinter as tk
from tkinter.messagebox import *
from tkinter.filedialog import *

class MenuBar():
    def __init__(self, _root: 'tk.Tk()', MainWindow: 'MainWindow'):
        self._root: 'tk.Tk()' = _root
        self.menubar: 'tk.Menu' = tk.Menu(_root)
        self.filemenu: 'tk.Menu' = tk.Menu(self.menubar, tearoff=0)
        self.editmenu: 'tk.Menu' = tk.Menu(self.menubar, tearoff=0)
        self.toolmenu: 'tk.Menu' = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu: 'tk.Menu' = tk.Menu(self.menubar, tearoff=0)

        #########> FILE MENU <#########
        self.filemenu.add_command(label = "New", command = MainWindow.new_file) 
        self.filemenu.add_command(label = "Open", command = MainWindow.load_file) 
        self.filemenu.add_command(label = "Save", command = MainWindow.save_file) 
        self.filemenu.add_command(label = "Save as ...", command = lambda: MainWindow.save_file(True)) 
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = lambda: MainWindow.exit_(self._root)) 
        self.menubar.add_cascade(label = "File") 

        #########> EDIT MENU <#########
        self.editmenu.add_command(label = "Settings", command = MainWindow.configure_settings)
        self.menubar.add_cascade(label = "Edit") 

        #########> TOOL MENU <#########
        self.toolmenu.add_command(label = "Execute", command = lambda: None) #To-Do
        self.toolmenu.add_cascade(label = "Debug", menu = lambda: None) #To-Do
        self.toolmenu.add_cascade(label = "Build binary", menu = lambda: None) #To-Do
        self.toolmenu.add_cascade(label = "Build block scheme", menu = lambda: None) #To-Do
        self.menubar.add_cascade(label = "Tools") 

        #########> HELP MENU <#########
        self.helpmenu.add_command(label = "About PyEnlightenmentCode", command = lambda: None) #To-Do
        self.helpmenu.add_cascade(label = "License", menu = lambda: None) #To-Do
        self.menubar.add_cascade(label = "Help") 

        #########> CONFIG TO ROOT <#########
        self._root.config(menu = self.menubar) 
          
