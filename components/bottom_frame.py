import logging

import tkinter as tk
from tkinter import scrolledtext

class BottomPanel():
    def __init__(self, frame):
        self.text_area = scrolledtext.ScrolledText(frame)
        self.text_handler = TextHandler(self.text_area)
        #~ self.text_area.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        self.text_area.grid(row=0, column=0, sticky="nsew")
        logger = logging.getLogger()
        logger.addHandler(self.text_handler)

    def show_logging_handler(self):
        pass

    def show_console(self): #To-Do
        pass

class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tk.END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(tk.END)
        self.text.after(0, append)
