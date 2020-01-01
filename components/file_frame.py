import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import logging

from pygments import lex
from pygments.lexers import PythonLexer

from defaults.tkhelper import TkHelper

class EditorManager(ttk.Notebook):
    loaded_data = None

    def __init__(self, MainWindow, root, frame, *args, **kwargs):
        self.editor_frame = ttk.Frame(frame, *args, **kwargs)
        TkHelper.configure_grid_x(self.editor_frame, col=50, col_interval=1, weight=1)
        TkHelper.configure_grid_y(self.editor_frame, row=50, row_interval=1, weight=1)
        self.file_tabs = FileContent(MainWindow, root, self.editor_frame)
        self.editor_frame.pack(side=tk.TOP, fill = tk.X, expand=True)

    def new_file(self):
        pass

    def load_file(self, path):
        pass

    def save_file(self, path):
        pass

    def save_all_files(self):
        pass

    def update_tags(self):
        logging.debug("Updateing tags")
        self.text_area.tag_configure("for", background="yellow")

class FileContent(ttk.Frame):
    def __init__(self, MainWindow, root, frame, filename="New File", *args, **kwargs):
        self.frame = ttk.Frame(frame, *args, **kwargs)
        self.filename = filename
        self.text = ProgrammingText(frame, font="monospace 10")
        self.linenum = tk.Text(frame, font="monospace 10", width=3) #To-Do
        self.scroll = tk.Scrollbar(frame, command=self.text.yview or self.linenum.yview)
        
        self.text.configure(yscrollcommand=self.scroll.set)
        self.linenum.configure(yscrollcommand=self.scroll.set)
        #~ TkHelper.config_tags(self.text)
        #~ TkHelper.highligting(self.text, root, MainWindow)
        self.text.insert("end", "Select part of text and then click 'for'...\nfo")
        self.text.focus()
                           
        self.scroll.grid(row=1, rowspan=49, column=50, sticky="snew")
        self.text.grid(row=1, rowspan=49, column=1, columnspan=49, sticky="snew")
        self.linenum.tag_configure('line', justify='right') #To-Do
        self.linenum.config(state="disabled")
        self.linenum.grid(row=1, rowspan=10, column=0, sticky="snew") #To-Do
        
        root.bind("<Key>", lambda event: TkHelper.lazy_highligting(self.text))


class ProgrammingText(tk.Text):
    def highlight_pattern(self, pattern: str, tag: str, regexp: bool = False, #To rework
                          start: str = "1.0", end: str = "end") -> None:
        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            #~ if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", f"{index}+{count.get()}c")
            self.tag_add(tag, "matchStart", "matchEnd")

    def lazy_highligting(self: 'ProgrammingText', event: 'tk.Event' = None): #To improve efficiency
        logging.debug("running")
        self.mark_set("range_start", "1.0")
        data = self.get("1.0", "end-1c")
        for token, content in lex(data, PythonLexer()):
            self.mark_set("range_end", "range_start + %dc" % len(content))
            self.tag_add(str(token), "range_start", "range_end")
            self.mark_set("range_start", "range_end")

