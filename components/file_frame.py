import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import logging
                
import typing
from typing import List

import os

from components.editor_programming_text import ProgrammingText
from components.editor_execution_tools import ExecutionTools
from components.editor_debugger import Debugger

from defaults.tkhelper import Default
from defaults.tkhelper import TkHelper

class EditorManager():
    loaded_data: List['FileContent'] = None
    active_file: 'FileContent' = None

    def __init__(self, MainWindow: 'MainWindow', root: 'tk.Tk', frame: 'tk.Frame', *args: tuple, **kwargs: dict):
        self.editor_frame: 'ttk.Notebook' = ttk.Notebook(frame, *args, **kwargs)
        self.editor_frame.pack(side = tk.TOP, fill=tk.BOTH, expand = True)
        self.editor_frame._active = None
        if not self.loaded_data:
            self.loaded_data = []
            self.loaded_data.append(FileContent(MainWindow, root, self.editor_frame, "New File"))
            self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)
            
        self.MainWindow = MainWindow
        self.root = root
        root.bind("<KeyRelease>", lambda event: TkHelper.lazy_highligting(ProgrammingText.active_text) or ProgrammingText.update_linenumbers(), add="+")
        self.editor_frame.bind("<ButtonPress-2>", self.__on_close_press, True)
        self.editor_frame.bind("<ButtonRelease-2>", self.__on_close_release)

    def new_file(self):
        self.loaded_data.append(FileContent(self.MainWindow, self.root, self.editor_frame, "New File"))
        self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)

    def load_file(self):
        path = filedialog.askopenfilename(initialdir = Default.get("default_path"), title = "Select file", filetypes = (("python files","*.py"), ("all files", "*.*")))
        if not path:
            logging.info(f"Loading canceled"); return
        filename = path.split(os.path.sep)[-1]
        self.loaded_data.append(FileContent(self.MainWindow, self.root, self.editor_frame, filename))
        self.loaded_data[-1].path = path
        with open(path, "r") as opened_file:
            self.loaded_data[-1].add_content(opened_file.read())
            logging.info(self.editor_frame.tabs())
            self.loaded_data[-1].programming_text.update_linenumbers()
        self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)

    def save_file(self, as_new: bool = False):
        file_data: 'FileContent' = self.active_file
        if file_data.path is None:
            current_path = Default.get("default_path")
            logging.debug(f"Default, save path is {current_path}")
            path = filedialog.asksaveasfilename(initialdir = current_path,
                                                 title = "Select where to save file",
                                                 filetypes = (("python files", "*.py"), ("all files", "*.*")))
            if not path:
                logging.info(f"Saving canceled"); return
            logging.info(f"Saving as {path}")
            self.active_file.path = path
        elif as_new:
            current_path = f"{os.path.sep}".join(iter(self.active_file.path.split(os.path.sep)[:-1]))
            logging.debug(f"Default, save path is {current_path}")
            path = filedialog.asksaveasfilename(initialdir = current_path,
                                                 title = "Select where to save file",
                                                 filetypes = (("python files", "*.py"), ("all files", "*.*")))
            if not path:
                logging.info(f"Saving canceled"); return
            logging.info(f"Saving as {path}")
            self.active_file.path = path
        with open(self.active_file.path, "w") as saveing_file:
            saveing_file.write(self.active_file.programming_text.text.get("1.0", "end"))
        self.active_file.filename = self.active_file.path.split(os.path.sep)[-1]
        self.editor_frame.tab(self.active_file.frame, text=self.active_file.filename)
    
    def destroy_temp(self):
        ExecutionTools.clean_temp_files()

    @staticmethod
    def change_active_file(file_content):
        EditorManager.active_file = file_content
        logging.debug(f"Active file is changed to {file_content.filename}")

    def __on_close_press(self, event):
        element = self.editor_frame.identify(event.x, event.y)

        index = self.editor_frame.index("@%d,%d" % (event.x, event.y))
        self.editor_frame.state(['pressed'])
        self.editor_frame._active = index

    def __on_close_release(self, event):
        if not self.editor_frame.instate(['pressed']):
            return

        element =  self.editor_frame.identify(event.x, event.y)
        index = self.editor_frame.index("@%d,%d" % (event.x, event.y))

        if self.editor_frame._active == index:
            self.editor_frame.forget(index)
            self.editor_frame.event_generate("<<NotebookTabClosed>>")

        self.editor_frame.state(["!pressed"])
        self.editor_frame._active = None

class FileContent():
    def __init__(self, MainWindow: 'MainWindow', root: 'tk.Tk', notebook: 'ttk.Notebook', filename: str = "New File", path: str = None, *args: tuple, **kwargs: dict):
        self.filename: str = filename
        self.path: str = None
        
        self.frame: 'ttk.Notebook' = ttk.Notebook(notebook, *args, **kwargs)
        self.frame.pack(side = tk.TOP, fill = tk.BOTH)
        
        self.programming_text: 'ProgrammingText' = ProgrammingText(self.frame)
        self.programming_text.pack(fill = tk.BOTH, expand = True)
        code_object = self.programming_text.text
        self.execution_tools: 'ExecutionTools' = ExecutionTools(self.frame, code_object)
        self.execution_tools.pack(fill = tk.BOTH, expand = True)

        self.frame.add(self.programming_text, text="Code")
        self.frame.add(self.execution_tools, text="Tools")
        
        self.frame.bind("<Visibility>", lambda event: EditorManager.change_active_file(self))

    def add_content(self, content):
        self.programming_text.add_content(content)
