import os
import sys
import typing
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
    def configure_grid_x(frame: Type['tk.Tk'], col: int = 1,
                         col_interval: int = 1, weigh: int = 1) -> None:
        for x in range(col*col_interval):
            Grid.columnconfigure(frame, x, weight=weigh)

    @staticmethod
    def configure_grid_y(frame: Type['tk.Tk'], row: int = 1,
                         row_interval: int = 1, weigh: int = 1) -> None:
        for y in range(row*row_interval):
            Grid.columnconfigure(frame, y, weight=weigh)

    @staticmethod
    def save_position(root: Type['tk.Tk']) -> None:
        x, y, wind_x, wind_y = (int(i) for i in re.split('\D+', root.winfo_geometry()))
        Default.set("x", x)
        Default.set("y", y)
        Default.set("wind_x", wind_x)
        Default.set("wind_y", wind_y)

class Default():
    PATH = os.path.join(os.path.expanduser("~"), ".config", "PyEnlightenmentCode")
    CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".config", "PyEnlightenmentCode", ".config.json")
    defaults = {"darkmode": True}

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
