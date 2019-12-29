import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from defaults.tkhelper import TkHelper

class EditorManager(ttk.Notebook):
    def __init__(self, MainWindow, root, frame, *args, **kwargs):
        self.editor_frame = ttk.Frame(frame, *args, **kwargs)
        TkHelper.configure_grid_x(self.editor_frame, col=10, weight=1)
        TkHelper.configure_grid_y(self.editor_frame, row=10, weight=1)
        self.file_tabs = FileContent(MainWindow, root, self.editor_frame)
        self.editor_frame.pack(side=tk.TOP, fill = tk.BOTH, expand=True)

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
        self.scroll = tk.Scrollbar(frame, command=self.text.yview)
        
        self.text.configure(yscrollcommand=self.scroll.set)
        TkHelper.config_tags(self.text)
        TkHelper.highligting(self.text, root, MainWindow)
        self.text.insert("end", "Select part of text and then click 'for'...\nfo")
        self.text.focus()
                           
        self.scroll.grid(row=1, rowspan=10, column=10, sticky="snew")
        self.text.grid(row=1, rowspan=10, column=0, columnspan=10, sticky="snew")
        

class ProgrammingText(tk.Text):
    def highlight_pattern(self, pattern: str, tag: str, regexp: bool = False,
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
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", f"{index}+{count.get()}c")
            self.tag_add(tag, "matchStart", "matchEnd")

