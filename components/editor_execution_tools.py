import tkinter as tk
from tkinter import ttk
import typing

from defaults.tkhelper import TkHelper
from defaults.tkhelper import Default
import logging

import os

# For pythontutor
import urllib.parse # Code to url
import webbrowser # Run browser

# For debugging
import tempfile # Tempfile to debug
import threading # Run another thread
import subprocess # Run command


class ExecutionTools(tk.Frame):
    active_block: 'TkCodeExecutors' = None
    def __init__(self, frame, code_object, *args, **kwargs):
        super().__init__(frame, *args, **kwargs)
        
        self.block: 'TkCodeExecutors' = TkCodeExecutors(self, code_object)
        if self.active_block is None:
            self.active_block = self.block

        self.block.pack(fill = tk.BOTH, expand = True)

        self.bind("<Visibility>", lambda event: ExecutionTools.change_active_block(self.block))
        
    @classmethod
    def change_active_block(cls, code_canvas):
        cls.active_block = code_canvas

    @staticmethod
    def clean_temp_files():
        for tmp_file in TkCodeExecutors.tmp_files_to_delete:
            try:
                os.remove(tmp_file)
                logging.info(f"Deleting temporary file: {tmp_file}")
            except FileNotFoundError:
                pass

class TkCodeExecutors(tk.Frame):
    pythontutor_site_prefix = "http://pythontutor.com/visualize.html#code="
    pythontutor_site_postfix = "&cumulative=false&curInstr=0&heapPrimitives=nevernest&mode=display&origin=opt-frontend.js&py=py3anaconda&rawInputLstJSON=%5B%5D&textReferences=false"
    tmp_files_to_delete = []

    def __init__(self, frame, code_object, *args, **kwargs):
        super().__init__(frame, *args, **kwargs)
        self.selector1: 'ttk.Button' = ttk.Button(self, text="Check code at Pythontutor", command=self.open_pythontutor)
        self.selector1.pack(side=tk.TOP, fill="both", expand = True)
        #~ self.selector1.grid(row=0, column=0, sticky="snew")
        self.selector2: 'ttk.Button' = ttk.Button(self, text="Check code locally", command=self.compile_errors)
        #~ self.selector2.grid(row=1, column=0, sticky="snew")
        self.selector2.pack(side=tk.TOP, fill="both", expand = True)
        self.selector3: 'ttk.Button' = ttk.Button(self, text="Check code with debugging tool", command=self.run_with_pdb)
        self.selector3.pack(side=tk.TOP, fill="both", expand = True)
        #~ self.selector3.grid(row=2, column=0, sticky="snew")
        self.selector4: 'ttk.Button' = ttk.Button(self, text="Execute code", command=self.execute_code)
        self.selector4.pack(side=tk.TOP, fill="both", expand = True)
        #~ self.selector4.grid(row=3, column=0, sticky="snew")
        self.code_object = code_object
        
    def open_pythontutor(self):
        code = self.code_object.get("1.0",'end-1c')
        try:
            compile(code, "your_code", mode='exec')
        except SyntaxError as se:
            logging.error(f"Syntax error at line {se.__traceback__.tb_lineno}, you can't check this code.")
            return None
        formated_code = urllib.parse.quote(code)
        link = f"{self.pythontutor_site_prefix}{formated_code}{self.pythontutor_site_postfix}"
        webbrowser.open_new(link)
        
    def compile_errors(self):
        code = self.code_object.get("1.0",'end-1c')
        try:
            compile(code, "your_code", mode='exec')
        except Exception as ex:
            logging.error(f"{type(ex).__name__} at line {ex.__traceback__.tb_lineno}, you can't check this code.")
            logging.error(ex)
            return None
        logging.info(f"Code is correct to execute")

    def run_with_pdb(self):
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
            code = self.code_object.get("1.0",'end-1c')
            tmp_file.write(bytes(code, 'utf-8'))
            terminal = Default.get("terminal")
            debug_tool = Default.get("debug")
            execute = f"{terminal} -e {debug_tool} {tmp_file.name}"
            logging.info(f"Running: {execute}")
            TkCodeExecutors.tmp_files_to_delete.append(tmp_file.name)
            subprocess.run(execute, shell=True, universal_newlines=True)
            
    def execute_code(self):
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
            code = self.code_object.get("1.0",'end-1c')
            code += "\ninput(\"\"\"\n\n\"\"\"+\"-\"*40+\"\"\"\nClick enter to close\"\"\")\n"
            tmp_file.write(bytes(code, 'utf-8'))
            terminal = Default.get("terminal")
            executor = Default.get("execute")
            execute = f"{terminal} -e {executor} {tmp_file.name}"
            logging.info(f"Running: {execute}")
            TkCodeExecutors.tmp_files_to_delete.append(tmp_file.name)
            subprocess.run(execute, shell=True, universal_newlines=True)

