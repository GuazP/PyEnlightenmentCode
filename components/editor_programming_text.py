import tkinter as tk
from tkinter import ttk

import typing

import logging

from defaults.tkhelper import TkHelper
from defaults.tkhelper import Default

example_code = """import math

for i in range(100):
    j = math.sqrt(i)
"""

class ProgrammingText(tk.Frame):
    active_text: 'TkHighlightningText' = None
    active_linenum: 'tk.Text' = None
    
    def __init__(self, template: bool = False, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        
        self.text: 'TkHighlightningText' = TkHighligtningText(self, font="monospace 10")
        if Default.get("darkmode", True):
            self.text.config(insertbackground="white", exportselection=True)
        if self.active_text is None:
            self.active_text = self.text
        TkHelper.config_tags(self)
        #~ self.text.insert("end", example_code)
        #~ self.text.insert("end", "for some range as example 'of' 9.75 examples in \"code\" # And there is a comment ;)")
        #~ self.text.insert("end", "\n#line nr. "+"\n#line nr. ".join(str(i) for i in range(6, 50)))
        self.text.focus()

        self.linenum: 'tk.Text' = tk.Text(self, font="monospace 10", width=4) #To-Do
        #~ self.linenum: 'tk.Text' = TextLineNumbers(self, font="monospace 10", width=4) #To-Do
        self.linenum.tag_configure('line', justify='right') #To-Do
        lines = int(self.text.index('end').split('.')[0])
        self.linenum.insert("end", "\n".join(str(i) for i in range(1, lines)))
        self.linenum.config(state = "disabled")
        #~ self.linenum.attach(self.text)

        self.scroll: 'tk.Scrollbar' = ttk.Scrollbar(self, command = self.__scrollBoth)
        self.text.config(yscrollcommand=self.__updateScroll)
        self.linenum.config(yscrollcommand=self.__updateScroll)

        self.scroll.pack(side = tk.RIGHT, fill = tk.Y)
        self.linenum.pack(side = tk.LEFT, fill = tk.Y) #To-Do      
        self.text.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        #~ self.bind('<<Selection>>', lambda event: ProgrammingText.select_range(self.text, "1.0", "end"))
        self.text.bind("<Visibility>", lambda event: ProgrammingText.change_active_text(self.text, self.linenum))
        #~ self.bind("<<Modified>>", lambda event: TkHelper.lazy_highligting(ProgrammingText.active_text))
        #~ self.bind("<KeyRelease>", lambda event: TkHelper.lazy_highligting(ProgrammingText.active_text))
        
    @staticmethod
    def change_active_text(programming_text, linenum):
        TkHelper.remove_highlighting(ProgrammingText.active_text)
        ProgrammingText.active_linenum = linenum
        ProgrammingText.active_text = programming_text
        TkHelper.lazy_highligting(ProgrammingText.active_text, typed = False)
        ProgrammingText.update_linenumbers()

    @staticmethod
    def update_linenumbers():
        lines_text = int(ProgrammingText.active_text.index('end').split('.')[0])
        lines_nums = int(ProgrammingText.active_linenum.index('end').split('.')[0])
        logging.debug(f"Text widget contain {lines_text} lines.")
        logging.debug(f"Linenumber widget contain {lines_nums} lines.")
        ProgrammingText.active_linenum.config(state = "normal")
        if lines_text > lines_nums :
            logging.debug(f"Adding lines to line numbers: {range(lines_nums, lines_text)}")
            ProgrammingText.active_linenum.insert("end", "\n"+"\n".join(str(i) for i in range(lines_nums, lines_text)))
        elif lines_text < lines_nums:
            logging.debug(f"Removing line numbers after: {lines_text}")
            ProgrammingText.active_linenum.delete(f"{lines_text}.0", "end")
        ProgrammingText.active_linenum.config(state = "disabled")

    def add_content(self, content):
        self.text.insert("end", content)
        ProgrammingText.update_linenumbers()

    def __scrollBoth(self, action, position, type=None):
        self.text.yview_moveto(position)
        self.linenum.yview_moveto(position)

    def __updateScroll(self, first, last, type=None):
        self.text.yview_moveto(first)
        self.linenum.yview_moveto(first)
        self.scroll.set(first, last)

class TkHighligtningText(tk.Text):
    def highlight_pattern(self, pattern: str, tag: str, regexp: bool = False,
                          start: str = "1.0", end: str = "end",
                          exclude_first: bool = False) -> None:
        start: str = self.index(start)
        end: str = self.index(end)
        self.mark_set("mStart", start)
        self.mark_set("mEnd", start)
        self.mark_set("sLimit", end)

        count: 'tk.IntVar' = tk.IntVar()
        index: str = self.search(pattern, "mEnd","sLimit",
                                 count=count, regexp=regexp)
        while index:
            length = count.get()
            self.mark_set("mStart", f"{index}")
            self.mark_set("mEnd", f"{index}+{length}c")
            self.tag_add(tag, "mStart", "mEnd")
            index: str = self.search(pattern, "mEnd","sLimit",
                                     count=count, regexp=regexp)
