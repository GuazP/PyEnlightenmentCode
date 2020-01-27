import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import *
from tkinter.filedialog import *

class MenuBar():
    def __init__(self, _root: 'tk.Tk()', MainWindow: 'MainWindow'):
        self._root: 'tk.Tk()' = _root
        self.menubar: 'tk.Menu' = tk.Menu(_root)
        self.filemenu: 'tk.Menu' = tk.Menu(_root, tearoff=0)
        self.editmenu: 'tk.Menu' = tk.Menu(_root, tearoff=0)
        #~ self.toolmenu: 'tk.Menu' = tk.Menu(_root, tearoff=0)
        self.helpmenu: 'tk.Menu' = tk.Menu(_root, tearoff=0)

        #########> FILE MENU <#########
        self.filemenu.add_command(label = "New", command = MainWindow.new_file) 
        self.filemenu.add_command(label = "Open", command = MainWindow.load_file) 
        self.filemenu.add_command(label = "Save", command = MainWindow.save_file) 
        self.filemenu.add_command(label = "Save as ...", command = lambda: MainWindow.save_file(as_new = True)) 
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command = lambda: MainWindow.exit_(self._root)) 
        self.menubar.add_cascade(label = "File", menu = self.filemenu) 

        #########> EDIT MENU <#########
        self.editmenu.add_command(label = "Settings", command = MainWindow.configure_settings)
        self.menubar.add_cascade(label = "Edit", menu = self.editmenu) 

        #########> TOOL MENU <#########
        #~ self.toolmenu.add_command(label = "Execute", command = lambda: None) #To-Do
        #~ self.toolmenu.add_cascade(label = "Debug", command = lambda: None) #To-Do
        #~ self.toolmenu.add_cascade(label = "Build binary", command = lambda: None) #To-Do
        #~ self.toolmenu.add_cascade(label = "Build block scheme", command = lambda: None) #To-Do
        #~ self.menubar.add_cascade(label = "Tools", menu = self.toolmenu) 

        #########> HELP MENU <#########
        self.helpmenu.add_command(label = "About PyEnlightenmentCode", command = lambda: None) #To-Do
        self.helpmenu.add_cascade(label = "License", command = lambda: None) #To-Do
        self.menubar.add_cascade(label = "Help", menu = self.helpmenu) 

        #########> CONFIG TO ROOT <#########
        self._root.config(menu = self.menubar) 
          
