import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import logging
                
import typing
from typing import List

from components.editor_programming_text import ProgrammingText
from components.editor_code_block import CodeBlock
from components.editor_debugger import Debugger
from defaults.tkhelper import TkHelper

class EditorManager():
    loaded_data: List['FileContent'] = None

    def __init__(self, MainWindow: 'MainWindow', root: 'tk.Tk', frame: 'tk.Frame', *args: tuple, **kwargs: dict):
        self.editor_frame: 'ttk.Notebook' = ttk.Notebook(frame, *args, **kwargs)
        self.editor_frame.pack(fill=tk.BOTH)
        if not self.loaded_data:
            self.loaded_data = []
            self.loaded_data.append(FileContent(MainWindow, root, self.editor_frame, "New File"))
            self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)
            self.loaded_data.append(FileContent(MainWindow, root, self.editor_frame, "New File"))
            self.editor_frame.add(self.loaded_data[-1].frame, text = self.loaded_data[-1].filename)

        root.bind("<KeyRelease>", lambda event: TkHelper.lazy_highligting(ProgrammingText.active_text))

    def new_file(self):
        pass

    def load_file(self, path):
        pass

    def save_file(self, path):
        pass

    def save_all_files(self):
        pass

class FileContent():
    def __init__(self,MainWindow: 'MainWindow', root: 'tk.Tk', notebook: 'ttk.Notebook', filename: str = "New File", *args: tuple, **kwargs: dict):
        self.filename: str = filename
        
        self.frame: 'ttk.Notebook' = ttk.Notebook(notebook, *args, **kwargs)
        self.frame.pack(fill=tk.BOTH)
        
        self.programming_text: 'ProgrammingText' = ProgrammingText(self.frame)
        self.programming_text.pack(fill=tk.BOTH)
        #ToDo next frame with block scheme
        self.block_scheme: 'CodeBlock' = CodeBlock(self.frame)
        self.block_scheme.pack(fill=tk.BOTH)
        #ToDo next frame with debuger scheme
        self.debugger_frame: 'Debugger' = Debugger(self.frame)
        self.debugger_frame.pack(fill=tk.BOTH)

        self.frame.add(self.programming_text, text="Code")
        self.frame.add(self.block_scheme, text="Block")
        self.frame.add(self.debugger_frame, text="Debugger")
