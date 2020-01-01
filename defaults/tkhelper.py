import os
import sys
import typing
import tkinter as tk
#~ from tkinter.ttk import Font
from typing import Type
from typing import List
import logging
import re

import json


class TkHelper():
    @staticmethod
    def configure_window(root: Type['tk.Tk'], title: str = "Noname") -> None:
        #Title
        root.title(title)
        
        #Screen size
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        logging.debug(f"Readed screen resolution is {screen_width}x{screen_height}")

        #Windowplacement
        root.overrideredirect(0)
        min_x = int(root.winfo_screenwidth()/8)
        min_y = int(root.winfo_screenheight()/8)
        
        x = int(Default.get("x", screen_width))
        y = int(Default.get("y", screen_height))
        
        wind_x = Default.get("wind_x", int((screen_width-x)/2))
        if wind_x < 0 or wind_x > screen_width-10:
            wind_x = int((screen_width-x)/2)
        Default.set("wind_x", wind_x)
        wind_y = Default.get("wind_y", int((screen_height-y)/2))
        if wind_y < 0 or wind_y > screen_height-10:
            wind_y = int((screen_height-y)/2)
        Default.set("wind_y", wind_y)
        
        root.geometry(f"{x}x{y}+{wind_x}+{wind_y}")
        root.minsize(min_x, min_y)
        root.maxsize(screen_width, screen_height)
        logging.debug(f"Geometry is set to: {x}x{y}+{wind_x}+{wind_y}")

        root.focus_set()

    @staticmethod
    def configure_visual(master: Type['tk.Tk'], darkmode: bool = True,
                         *args: List[str]) -> None:
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
    def config_tags(text: Type['ProgrammingText']) -> None:
        prefix = "d" if Default.get("darkmode") else "b"
        normal_font = Default.get("basic_font")
        bolded_font = Default.get("highlight_font")
        text.tag_config("normal", foreground=Default.get(prefix+"font_color_normal", '#FFFFFF'), font=normal_font)
        text.tag_config("chain_grammar", foreground=Default.get(prefix+"font_color_chain", '#FFFF4E'), font=bolded_font)
        for cg in Default.chain_gramar:
            text.highlight_pattern(cg, "chain_grammar")
        text.tag_config("builtin_func", foreground=Default.get(prefix+"font_color_builtin", '#4EE6FF'), font=bolded_font)
        for bf in Default.builtin_func:
            text.highlight_pattern(bf, "builtin_func")
        text.tag_config("digits", foreground=Default.get(prefix+"font_color_digits", '#D0762D'), font=bolded_font)
        text.tag_config("one-line-string", foreground=Default.get(prefix+"font_color_string", '#001DA6'), font=normal_font)
        text.tag_config("multi-line-string", foreground=Default.get(prefix+"font_color_mstring", '#B42A63'), font=normal_font)
        #~ text.tag_config("class-name", foreground=Default.get("font_color_class", '#FFF500'), font=Default.basic_font) #To-Do
        #~ text.tag_config("func-name", foreground=Default.get("font_color_func", '#FFF95C'), font=Default.basic_font) #To-Do

    #~ @staticmethod
    #~ def highligting(text: Type['ProgrammingText'], root: Type['tk.Tk'], MainWindow: Type['MainWindow']) -> None:
        #~ '''Junk method needs to be optymalized only for actual fragment on actual file and already copied file
        #~ Still good as first call for file to catch tags'''
        #~ refresh_rate = 500
        ###> Patterns <### 
        #~ chain_pattern_detailed = r"\s+(" + r")|\s+(".join(iter(Default.chain_gramar)) + r")"
        #~ chain_pattern = r"|".join(iter(Default.chain_gramar))
        #~ builtin_pattern_detailed = r"(\s|\.)+(" + r")(\s|\(|\.)|(\s|\.)+(".join(iter(Default.builtin_func)) + r")(\s|\(|\.)"
        #~ builtin_pattern = r"|".join(iter(Default.builtin_func))

        #~ digits_pattern = r"\d|\d\.\d"
        
        #~ strings_pattern = r"(\"(.|\s)*\")|(\'(.|\s)*\')"
        ##~ multi_strings_pattern = r"\d|\d\.\d"
        
        ##~ MainWindow.add_to_mainloop(root, time=refresh_rate,
                                   #~ func=lambda: [text.tag_remove(tag, "1.0", "end") for tag in text.tag_names()])
        ##~ logging.debug(f"Running mainloop font_normal per {refresh_rate/1000}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate,
                                   #~ func=lambda: text.highlight_pattern(pattern=chain_pattern,
                                                                       #~ tag="chain_grammar", regexp=True))
        #~ logging.debug(f"Running mainloop font_chain per {refresh_rate/1000}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate,
                                   #~ func=lambda: text.highlight_pattern(pattern=builtin_pattern,
                                                                       #~ tag="builtin_func", regexp=True))
        #~ logging.debug(f"Running mainloop font_builtin per {refresh_rate/1000}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate,
                                   #~ func=lambda: text.highlight_pattern(pattern=digits_pattern,
                                                                       #~ tag="digits", regexp=True))
        #~ logging.debug(f"Running mainloop font_digits per {refresh_rate/1000}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate,
                                   #~ func=lambda: text.highlight_pattern(pattern=strings_pattern,
                                                                       #~ tag="one-line-string", regexp=True))
        #~ logging.debug(f"Running mainloop font_digits per {refresh_rate/1000}s")
        
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate*20,
                                   #~ func=lambda: [text.tag_remove(tag, "1.0", "end") for tag in text.tag_names()])
        #~ logging.debug(f"Running mainloop font_normal per {refresh_rate/50}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate*20,
                                   #~ func=lambda: text.highlight_pattern(pattern=chain_pattern_detailed,
                                                                       #~ tag="chain_grammar", regexp=True))
        #~ logging.debug(f"Running mainloop font_chain_precise per {refresh_rate/50}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate*20,
                                   #~ func=lambda: text.highlight_pattern(pattern=builtin_pattern_detailed,
                                                                       #~ tag="builtin_func", regexp=True))
        #~ logging.debug(f"Running mainloop font_builtin_precise per {refresh_rate/50}s")
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate*20,
                                   #~ func=lambda: text.highlight_pattern(pattern=digits_pattern,
                                                                       #~ tag="digits", regexp=True))
        #~ MainWindow.add_to_mainloop(root, time=refresh_rate*20,
                                   #~ func=lambda: text.highlight_pattern(pattern=strings_pattern,
                                                                       #~ tag="one-line-string", regexp=True))

    @staticmethod
    def lazy_highligting(text: Type['ProgrammingText']) -> None:
        pass

class Default():
    #Settings
    PATH = os.path.join(os.path.expanduser("~"), ".config", "PyEnlightenmentCode")
    CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "PyEnlightenmentCode", ".config.json")
    defaults = {"execute": "python3",                           #Interpreter
                "debug": "python3 -m pdb",                      #Debuger
                "binary": "pyinstaller",                        #'Compiler'
                "basic_font": "monospace 10",                   #Basic Font
                "highlight_font": "monospace 10 bold",          #Bolded Font
                "darkmode": True                                #General color mode
                }
    defaults.update({
                "dfont_color_normal": '#FFFFFF',                #Dark normal color
                "bfont_color_normal": '#000000',                #Bright normal color
                "dfont_color_chain": '#FFFF4E',                 #Dark chain color
                "bfont_color_chain": '#0000B1',                 #Bright chain color
                "dfont_color_builtin": '#4EE6FF',               #Dark builtin color
                "bfont_color_builtin": '#B11900',               #Bright chain color
                "dfont_color_digits": '#D0762D',                #Dark digits color
                "bfont_color_digits": '#3F89D2',                #Bright digits color
                "dfont_color_string": '#001DA6',                #Dark string color
                "bfont_color_string": '#5D3A1E',                #Bright string color
                "dfont_color_mstring": '#B42A63',               #Dark multiline string color
                "bfont_color_mstring": '#4BD59C'                #Bright multiline string color
                })

    #Grammar
    chain_gramar = ['False', 'class', 'finally', 'is', 'return',
                    'None', 'continue', 'for', 'lambda', 'try',
                    'True', 'def', 'from', 'nonlocal', 'while',
                    'and', 'del', 'global', 'not', 'with',
                    'as', 'elif', 'if', 'or', 'yield',
                    'assert', 'else', 'import', 'pass',
                    'break', 'except', 'in', 'raise']
    builtin_func = ['abs()', 'delattr', 'hash', 'memoryview', 'set',
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
    strings = ['\'', '\"']
    func_declarations = []
    class_declarations = []

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
        return cls.defaults.get(attr, default)

    @classmethod
    def set(cls: Type['Default'], attr: str, value: object,
            alternative: object = None) -> None:
        cls.defaults[attr] = value if not (value is None) else alternative
        logging.debug(f"`{attr}` is set to `{cls.defaults[attr]}` in Default")

    @classmethod
    def save(cls: Type['Default']) -> None:
        file_path = Default.CONFIG_PATH
        path = Default.PATH
        if not os.path.exists(path):
            logging.debug(f"Creating path {path}.")
            os.makedirs(path)
        with open(file_path, "w") as configs:
            configs.write(json.dumps(cls.defaults))
        logging.debug(f"Save configs in `{file_path}` is sucessful.")

    @classmethod
    def load(cls: Type['Default']) -> Type['Default']:
        file_path = Default.CONFIG_PATH
        path = Default.PATH
        if not os.path.exists(path):
            logging.debug(f"Creating path {path}.")
            os.makedirs(path)
        if os.path.exists(file_path):
            logging.debug(f"Configs found, loading binary data")
            with open(file_path, "r") as configs:
                defaults = json.loads(configs.read())
            cls.defaults = defaults
        else:
            logging.debug(f"Configs not found, loading Default as configs.")
            Default.save()
        return Default
