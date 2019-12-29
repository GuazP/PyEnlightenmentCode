import logging

import tkinter as tk
from tkinter import scrolledtext

class BottomPanel():
    def __init__(self, frame):
        self.selector1 = tk.Button(frame, text="Editor Info")
        self.selector1.grid(row=0, column=0, sticky="snew")
        self.text_area = scrolledtext.ScrolledText(frame, height=10)
        self.text_handler = TextHandler(self.text_area)
        self.text_area.grid(row=0, column=1, rowspan = 3, columnspan=6, sticky="snew")
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
