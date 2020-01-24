import typing
from typing import Dict

import logging

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from defaults.tkhelper import Default

class BottomPanel():
    def __init__(self, frame: 'ttk.Frame'):
        self.selector1: 'ttk.Button' = ttk.Button(frame, text="Editor Info")
        self.selector1.grid(row=0, column=0, sticky="snew")
        self.text_area: 'scrolledtext.ScrolledText' = scrolledtext.ScrolledText(frame, height=10)
        self.text_handler: 'TextHandler' = TextHandler(self.text_area)
        self.text_area.grid(row=0, column=1, rowspan = 3, columnspan=6, sticky="snew")
        logger: 'logging' = logging.getLogger()
        logger.addHandler(self.text_handler)

    def show_logging_handler(self):
        pass

    def show_console(self): #To-Do
        pass

class TextHandler(logging.Handler):
    tag_level: Dict[str, str] = {
            "CRITICAL": "#0000FF",
            "ERROR": "#FF0000",
            "WARNING": "#AA1111",
            "INFO": "#FFFFFF",
            "DEBUG": "#00FF00",
            "NOTSET": "#303030"}
    
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text: 'scrolledText.ScrolledText' = text
        formatter: 'logging.Formatter' = logging.Formatter('%(levelname)-8s %(message)s')
        self.setFormatter(formatter)
        for tag, color in self.tag_level.items():
            self.text.tag_config(tag, foreground=color)
        
    def emit(self, record):
        msg: str = self.format(record)
        def append():
            print(msg)
            for tag in self.tag_level:
                if msg.strip().startswith(tag):
                    self.text.configure(state='normal')
                    self.text.insert(tk.END, msg + '\n', tag)
                    self.text.configure(state='disabled')
                    self.text.yview(tk.END)
                    break
            else:
                logging.error("Logging type unrecognized for {msg}")
        self.text.after(0, append)
