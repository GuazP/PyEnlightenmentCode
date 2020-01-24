import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import logging
                
import typing
from typing import List

import os

from components.editor_programming_text import ProgrammingText
from components.editor_code_block import CodeBlock
from components.editor_debugger import Debugger

from defaults.tkhelper import Default
from defaults.tkhelper import TkHelper

class EditorManager():
    loaded_data: List['FileContent'] = None
    active_file: 'FileContent' = None

    def __init__(self, MainWindow: 'MainWindow', root: 'tk.Tk', frame: 'tk.Frame', *args: tuple, **kwargs: dict):
        self.editor_frame: 'ttk.Notebook' = ttk.Notebook(frame, *args, **kwargs)
        self.editor_frame.pack(side = tk.TOP, fill=tk.BOTH, expand = True)
        if not self.loaded_data:
            self.loaded_data = []
            self.loaded_data.append(FileContent(MainWindow, root, self.editor_frame, "New File"))
            self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)
            self.loaded_data.append(FileContent(MainWindow, root, self.editor_frame, "New File2"))
            self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)

        self.MainWindow = MainWindow
        self.root = root
        root.bind("<KeyRelease>", lambda event: TkHelper.lazy_highligting(ProgrammingText.active_text) or ProgrammingText.update_linenumbers(), "+")

    def new_file(self):
        self.loaded_data.append(FileContent(self.MainWindow, self.root, self.editor_frame, "New File"))
        self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)

    def load_file(self):
        path = filedialog.askopenfilename(initialdir = Default.get("default_path"), title = "Select file", filetypes = (("python files","*.py"), ("all files", "*.*")))
        filename = path.split(os.path.sep)[-1]
        self.loaded_data.append(FileContent(self.MainWindow, self.root, self.editor_frame, filename))
        self.loaded_data[-1].path = path
        with open(path, "r") as opened_file:
            self.loaded_data[-1].add_content(opened_file.read())
        self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)

    def save_file(self, as_new: bool = False):
        file_data: 'FileContent' = self.active_file
        if file_data.path is None:
            current_path = Default.get("default_path")
            logging.debug(f"Default, save path is {current_path}")
            path = filedialog.asksaveasfilename(initialdir = current_path,
                                                 title = "Select where to save file",
                                                 filetypes = (("python files", "*.py"), ("all files", "*.*")))
            logging.info(f"Saving as {path}")
            self.active_file.path = path
        elif as_new:
            current_path = f"{os.path.sep}".join(iter(path.split(os.path.sep)[:-1]))
            logging.debug(f"Default, save path is {current_path}")
            path = filedialog.asksaveasfilename(initialdir = current_path,
                                                 title = "Select where to save file",
                                                 filetypes = (("python files", "*.py"), ("all files", "*.*")))
            logging.info(f"Saving as {path}")
            self.active_file.path = path
        with open(self.active_file.path, "w") as saveing_file:
            saveing_file.write(self.active_file.programming_text.text.get("1.0", "end"))
    
    def save_all_files(self):
        pass

    @staticmethod
    def change_active_file(file_content):
        EditorManager.active_file = file_content
        logging.debug(f"Active file is changed to {file_content.filename}")

class FileContent():
    def __init__(self, MainWindow: 'MainWindow', root: 'tk.Tk', notebook: 'ttk.Notebook', filename: str = "New File", path: str = None, *args: tuple, **kwargs: dict):
        self.filename: str = filename
        self.path: str = None
        
        self.frame: 'ttk.Notebook' = ttk.Notebook(notebook, *args, **kwargs)
        self.frame.pack(side = tk.TOP, fill = tk.BOTH)
        
        self.programming_text: 'ProgrammingText' = ProgrammingText(self.frame)
        self.programming_text.pack(fill = tk.BOTH, expand = True)
        code_object = self.programming_text.text
        #ToDo next frame with block scheme
        self.block_scheme: 'CodeBlock' = CodeBlock(self.frame, code_object)
        self.block_scheme.pack(fill = tk.BOTH, expand = True)
        #ToDo next frame with debuger scheme
        self.debugger_frame: 'Debugger' = Debugger(self.frame)
        self.debugger_frame.pack(fill = tk.BOTH, expand = True)

        self.frame.add(self.programming_text, text="Code")
        self.frame.add(self.block_scheme, text="Block")
        self.frame.add(self.debugger_frame, text="Tools")
        
        self.frame.bind("<Visibility>", lambda event: EditorManager.change_active_file(self))

    def add_content(self, content):
        self.programming_text.add_content(content)
