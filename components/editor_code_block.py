import tkinter as tk
from tkinter import ttk
import typing

from defaults.tkhelper import TkHelper

class CodeBlock(tk.Frame):
    active_block: 'TkCodeCanvas' = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.block: 'TkCodeCanvas' = TkCodeCanvas(self)
        if self.active_block is None:
            self.active_block = self.block

        self.bind("<Visibility>", lambda event: CodeBlock.change_active_block(self.block))
        
    @classmethod
    def change_active_block(cls, code_canvas):
        cls.active_block = code_canvas

class TkCodeCanvas(tk.Canvas):
    pass
