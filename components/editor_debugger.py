import tkinter as tk
from tkinter import ttk

import typing
from typing import Dict

import logging

from defaults.tkhelper import TkHelper

class Debugger(tk.Frame):
    ### To-Do | Do this through tempfile to prevent user from accident override.
    active_debuggers: Dict[str, 'Debugger'] = {}
    active_debugger: 'Debugger' = None
    
    def __init__(self, filepath: str = None, content: str = None, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)

        if not filepath and not content:
            logging.error("No content available for debugging.")
            return

        self.filepath: str = filepath
        self.content: str = content

        self.frame: 'tk.Frame' = tk.Frame(self)
        if not (filepath in self.active_debuggers):
            self.active_debuggers[filepath] = self

        self.bind("<Visibility>", lambda event: Debugger.change_active_debugger(self.filepath))
        
    @classmethod
    def change_active_debugger(cls, filepath):
        cls.active_debugger = cls.active_debuggers[filepath]
