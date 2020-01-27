import os
import sys

import tkinter as tk

import typing
from typing import Type
from typing import List
from typing import Dict

import logging
import re
import json


class TkHelper():
    @staticmethod
    def configure_window(root: Type['tk.Tk'], title: str = "Noname") -> None:
        #Title
        root.title(title)
        
        #Screen size
        screen_width: str = root.winfo_screenwidth()
        screen_height: str = root.winfo_screenheight()
        logging.debug(f"Readed screen resolution is {screen_width}x{screen_height}")

        #Windowplacement
        root.overrideredirect(0)
        min_x: int = int(root.winfo_screenwidth()/8)
        min_y: int = int(root.winfo_screenheight()/8)
        
        x: int = int(Default.get("x", screen_width))
        y: int = int(Default.get("y", screen_height))
        
        wind_x: int = Default.get("wind_x", int((screen_width-x)/2))
        if wind_x < 0 or wind_x > screen_width-10:
            wind_x = int((screen_width-x)/2)
        Default.set("wind_x", wind_x)
        wind_y: int = Default.get("wind_y", int((screen_height-y)/2))
        if wind_y < 0 or wind_y > screen_height-10:
            wind_y = int((screen_height-y)/2)
        Default.set("wind_y", wind_y)
        
        root.geometry(f"{x}x{y}+{wind_x}+{wind_y}")
        root.minsize(min_x, min_y)
        root.maxsize(screen_width, screen_height)
        logging.debug(f"Geometry is set to: {x}x{y}+{wind_x}+{wind_y}")

        root.focus_set()

    @staticmethod
    def configure_visual(master: Type['tk.Tk'], darkmode: bool = True, *args: List[str]) -> None:
        if darkmode:
            for name in args:
                master.option_add(f"*{name}.background", "black")
                master.option_add(f"*{name}.foreground", "white")
            logging.debug(f"DarkTheme is set for: {args}")
        else:
            for name in args:
                master.option_add(f"*{name}.background", "white")
                master.option_add(f"*{name}.foreground", "black")
            logging.debug(f"BrightTheme is set for: {args}")

    @staticmethod
    def configure_font(master: Type['tk.Tk'], font: str = 'monospace') -> None:
        pass

    @staticmethod
    def configure_grid_x(frame: Type['tk.Frame'], col: int = 1,
                         col_interval: int = 1, weight: int = 1) -> None:
        for x in range(col*col_interval):
            tk.Grid.columnconfigure(frame, x, weight=weight)

    @staticmethod
    def configure_grid_y(frame: Type['tk.Frame'], row: int = 1,
                         row_interval: int = 1, weight: int = 1) -> None:
        for y in range(row*row_interval):
            tk.Grid.columnconfigure(frame, y, weight=weight)

    @staticmethod
    def save_position(root: Type['tk.Tk']) -> None:
        x, y, wind_x, wind_y = (int(i) for i in re.split('\D+', root.winfo_geometry()))
        Default.set("x", x)
        Default.set("y", y)
        Default.set("wind_x", wind_x)
        Default.set("wind_y", wind_y)

    @staticmethod
    def config_tags(programming: Type['ProgrammingText']) -> None:
        prefix: str = "d" if Default.get("darkmode") else "b"
        normal_font: str = Default.get("basic_font")
        bolded_font: str = Default.get("highlight_font")
        programming.text.tag_config("normal", foreground=Default.get(prefix+"font_color_normal", '#FFFFFF'), font=normal_font)
        programming.text.tag_config("chain_grammar", foreground=Default.get(prefix+"font_color_chain", '#FFFF4E'), font=bolded_font)
        programming.text.tag_config("builtin_func", foreground=Default.get(prefix+"font_color_builtin", '#4EE6FF'), font=bolded_font)
        programming.text.tag_config("digits", foreground=Default.get(prefix+"font_color_digits", '#D0762D'), font=bolded_font)
        programming.text.tag_config("one-line-string", foreground=Default.get(prefix+"font_color_string", '#0026A1'), font=normal_font)
        programming.text.tag_config("multi-line-string", foreground=Default.get(prefix+"font_color_mstring", '#B42A63'), font=normal_font)
        #~ text.tag_config("class-name", foreground=Default.get("font_color_class", '#FFF500'), font=Default.basic_font) #To-Do
        #~ text.tag_config("func-name", foreground=Default.get("font_color_func", '#FFF95C'), font=Default.basic_font) #To-Do
        programming.text.tag_config("comments", foreground=Default.get(prefix+"font_color_comment", '#001DA6'), font=normal_font)

    @staticmethod
    def remove_highlighting(text: Type['ProgrammingText']) -> None:
        if not text:
            logging.warning("Text widget is None instead TkHighlightningText type.")
            return None
        iter(text.tag_remove(tag, "1.0", "end") for tag in text.tag_names())
            
    @staticmethod
    def lazy_highligting(text: Type['ProgrammingText'], typed: bool = True) -> None:
        """This highlightning should select adjusted region (pasted, or line where comes insertion)"""
        if not text:
            logging.warning("Text widget is None instead TkHighlightningText type.")
            return None
        logging.debug("Lazy highlightning runs")
        # ~ logging.debug()
        # Visualization https://www.debuggex.com/r/ | Testing https://regex101.com/
        # Note: Tkinter regex engine don't support Lookbehind asserts...
        chain_pattern_detailed: str = Default.chain_pattern_detailed
        builtin_pattern_detailed: str = Default.builtin_pattern_detailed
        digits_pattern: str = Default.digits_pattern
        strings_pattern: str = Default.strings_pattern
        mstrings_pattern: str = Default.mstrings_pattern
        comment_pattern: str = Default.comment_pattern

        if typed:
            line = int(text.index(tk.INSERT).split(".")[0])
            startline = f"{line-3}.0" if line > 3 else f"1.0"
            endingline = f"{line+3}.0"
        else:
            startline = "1.0"
            endingline = "end"
        for tag in text.tag_names():
            text.tag_remove(tag, startline, endingline)

        text.highlight_pattern(pattern=chain_pattern_detailed, start=startline, end=endingline, tag="chain_grammar", regexp=True)
        text.highlight_pattern(pattern=builtin_pattern_detailed, start=startline, end=endingline, tag="builtin_func", regexp=True)
        text.highlight_pattern(pattern=digits_pattern, start=startline, end=endingline, tag="digits", regexp=True)
        text.highlight_pattern(pattern=strings_pattern, start=startline, end=endingline, tag="one-line-string", regexp=True)
        text.highlight_pattern(pattern=comment_pattern, start=startline, end=endingline, tag="comments", regexp=True)
        logging.debug("Lazy highlightning ends")

class Default():
    #Settings
    PATH: str = os.path.join(os.path.expanduser("~"), ".config", "PyEnlightenmentCode")
    CONFIG_PATH: str = os.path.join(os.path.expanduser("~"), ".config", "PyEnlightenmentCode", ".config.json")
    #Basic settings
    defaults: Dict[str, object] = {
                "execute": "python3",                           #Interpreter
                "debug": "python3 -m pdb",                      #Debuger
                "binary": "pyinstaller",                        #'Compiler'
                "terminal": "x-terminal-emulator",              #Terminal emulator
                "default_path": os.path.expanduser("~/"),       #Default path
                "basic_font": "monospace 10",                   #Basic Font
                "highlight_font": "monospace 10 bold",          #Bolded Font
                "darkmode": True                                #General color mode
                }

    #Fonts color settings
    defaults.update({
                "dfont_color_normal": '#FFFFFF',                #Dark normal color
                "bfont_color_normal": '#000000',                #Bright normal color
                "dfont_color_chain": '#FFFF4E',                 #Dark chain color
                "bfont_color_chain": '#0000B1',                 #Bright chain color
                "dfont_color_builtin": '#4EE6FF',               #Dark builtin color
                "bfont_color_builtin": '#B11900',               #Bright chain color
                "dfont_color_digits": '#D0762D',                #Dark digits color
                "bfont_color_digits": '#3F89D2',                #Bright digits color
                "dfont_color_string": '#304FB4',                #Dark string color
                "bfont_color_string": '#5D3A1E',                #Bright string color
                "dfont_color_mstring": '#B42A63',               #Dark multiline string color
                "bfont_color_mstring": '#4BD59C',               #Bright multiline string color
                "dfont_color_comment": '#7CFFF7',               #Dark comments color
                "bfont_color_comment": '#6D2E00'                #Bright comments color
                })

    #Grammar
    chain_gramar: List[str] = [
                'False', 'class', 'finally', 'is', 'return',
                'None', 'continue', 'for', 'lambda', 'try',
                'True', 'def', 'from', 'nonlocal', 'while',
                'and', 'del', 'global', 'not', 'with',
                'as', 'elif', 'if', 'or', 'yield',
                'assert', 'else', 'import', 'pass',
                'break', 'except', 'in', 'raise']
    builtin_func: List[str] = [
                'abs', 'delattr', 'hash', 'memoryview', 'set',
                'all', 'dict', 'help', 'min', 'setattr', 'any',
                'dir', 'hex', 'next', 'slice', 'ascii', 'divmod',
                'id', 'object', 'sorted', 'bin', 'enumerate', 'input',
                'oct', 'staticmethod', 'bool', 'eval', 'int', 'open',
                'str', 'breakpoint', 'isinstance', 'ord', 'sum',
                'bytearray', 'filter', 'issubclass', 'pow', 'super',
                'bytes', 'float', 'iter', 'print', 'tuple', 'callable',
                'format', 'len', 'property', 'type', 'chr', 'frozenset',
                'list', 'range', 'vars', 'classmethod', 'getattr', 'locals',
                'repr', 'zip', 'compile', 'globals', 'map', 'reversed',
                '__import__', 'complex', 'hasattr', 'max', 'round']
    strings: List[str] = ['\'', '\"']
    func_declarations: str = []
    class_declarations: str = []

    
    # Visualization https://www.debuggex.com/r/ | Testing https://regex101.com/
    # Note: Tkinter regex engine don't support Lookbehind asserts...
    chain_pattern_detailed: str = r"(^|\s)?(" + r"|".join(iter(chain_gramar)) + r")(?=(\s|:|;|\())"
    builtin_pattern_detailed: str = r"(\s)+(" + r"|".join(iter(builtin_func)) + r")(?=(\s|\(|\.))"
    digits_pattern: str = r"(^|\[|\s|,|\(|\]|\})(\d+(\.\d+)?)(?=($|\s|,|\)|\]|}|;))" #Best would be: (^|(?<=[\b\s,\)]))(\d+(\.\d+)?)(?=($|\s|,|\)|\]|}|;))
    strings_pattern: str = r"(r|f)?(\"(.|\s)*\")|(\'(.|\s)*\')"
    mstrings_pattern: str = r"(r|f)?(\"{3}(.|\s)*\"{3})|(\'{3}(.|\s)*\'{3})"
    comment_pattern: str = r"#.*$"

    """Default config for MainFrame object, to separate code and store data"""
    def __init__(self: Type['Default'], parent: object) -> None:
        super().__setattr__('parent', parent)

    def __getattr__(self: Type['Default'], attr: str) -> object:
        return getattr(self.parent, attr)

    def __setattr__(self: Type['Default'], attr: str, value: object) -> None:
        if value is None:
            logging.debug(f"Can't load `{attr}`. Loading default `{attr}` as `{self.defaults.get(attr, None)}`.")
            self.parent.__setattr__(attr, self.defaults.get(attr, None))
        else:
            logging.debug(f"Loading `{attr}` as `{value}`")
            self.parent.__setattr__(attr, value)

    @classmethod
    def get(cls: Type['Default'], attr: str, default: object = None) -> object:
        value = cls.defaults.get(attr, default)
        logging.debug(f"`{attr}` as `{value}` is requested from Default")
        return value

    @classmethod
    def set(cls: Type['Default'], attr: str, value: object, alternative: object = None) -> None:
        cls.defaults[attr] = value if not (value is None) else alternative
        logging.debug(f"`{attr}` is set to `{cls.defaults[attr]}` in Default")

    @classmethod
    def save(cls: Type['Default']) -> None:
        file_path: str = Default.CONFIG_PATH
        path: str = Default.PATH
        if not os.path.exists(path):
            logging.debug(f"Creating path {path}.")
            os.makedirs(path)
        with open(file_path, "w") as configs:
            configs.write(json.dumps(cls.defaults))
        logging.debug(f"Save configs in `{file_path}` is sucessful.")

    @classmethod
    def load(cls: Type['Default']) -> Type['Default']:
        file_path: str = Default.CONFIG_PATH
        path: str = Default.PATH
        if not os.path.exists(path):
            logging.debug(f"Creating path {path}.")
            os.makedirs(path)
        if os.path.exists(file_path):
            logging.debug(f"Configs found, loading binary data")
            with open(file_path, "r") as configs:
                defaults = json.loads(configs.read())
            cls.defaults.update(defaults)
        else:
            logging.debug(f"Configs not found, loading Default as configs.")
            Default.save()
        return Default
