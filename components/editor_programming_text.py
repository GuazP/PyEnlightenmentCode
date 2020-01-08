import tkinter as tk
from tkinter import ttk

import typing

import logging

from defaults.tkhelper import TkHelper

class ProgrammingText(tk.Frame):
    active_text: 'TkHighlightningText' = None
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        
        self.text: 'TkHighlightningText' = TkHighligtningText(self, font="monospace 10")
        if not self.active_text:
            self.active_text = self.text
        TkHelper.config_tags(self)
        self.text.insert("end", "for some range as example 'of' 9.75 examples in \"code\" # And there is a comment ;)")
        self.text.insert("end", "\nline nr. "+"\nline nr. ".join(str(i) for i in range(2, 1000)))
        self.text.focus()

        self.linenum: 'tk.Text' = tk.Text(self, font="monospace 10", width=4) #To-Do
        self.linenum.tag_configure('line', justify='right') #To-Do
        self.linenum.insert("end", "\n".join(str(i) for i in range(1, 1000)))
        self.linenum.config(state = "disabled")

        self.scroll: 'tk.Text' = ttk.Scrollbar(self, command = self.text.yview or self.linenum.yview)
        self.text.configure(yscrollcommand = self.scroll.set)
        self.linenum.configure(yscrollcommand = self.scroll.set)

        self.scroll.pack(side = tk.RIGHT, fill = tk.Y)
        self.linenum.pack(side = tk.LEFT, fill = tk.Y) #To-Do      
        self.text.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        self.bind("<Visibility>", lambda event: ProgrammingText.change_active_text(self.text))
        
    @classmethod
    def change_active_text(cls, programming_text):
        TkHelper.remove_highlighting(cls.active_text)
        cls.active_text = programming_text
        TkHelper.lazy_highligting(cls.active_text)

class TkHighligtningText(tk.Text):
    def highlight_pattern(self, pattern: str, tag: str, regexp: bool = False,
                          start: str = "1.0", end: str = "end",
                          exclude_first: bool = False, exclude_last: bool = False) -> None:
        start: str = self.index(start)
        end: str = self.index(end)
        self.mark_set("mStart", start)
        self.mark_set("mEnd", start)
        self.mark_set("sLimit", end)

        count: 'tk.IntVar' = tk.IntVar()
        index: str = self.search(pattern, "mEnd","sLimit",
                                 count=count, regexp=regexp)
        while index:
            logging.error(index)
            length = count.get() -1 if exclude_last else count.get()
            self.mark_set("mStart", f"{index}")
            self.mark_set("mEnd", f"{index}+{length}c")
            self.tag_add(tag, "mStart", "mEnd")
            index: str = self.search(pattern, "mEnd","sLimit",
                                     count=count, regexp=regexp)
