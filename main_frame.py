#!/usr/bin/python3
from argparse import ArgumentParser

## MainFrame Tk namespace
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from ttkthemes import ThemedTk

## MainFrame typing namespace
import typing   
from typing import Type
from typing import List
from typing import Callable

## MainFrame libraries used
import logging
import os
import sys

## MainFrame using
from components.file_frame import EditorManager
from components.menu_frame import MenuBar
from components.bottom_frame import BottomPanel
from components.project_frame import ProjectManager

## MainFrame defaults and helper
from defaults.tkhelper import Default, TkHelper

class MainWindow(ttk.Frame):
    __instance: 'MainWindow' = None
    _root: 'ttk.Frame' = None
    _menubar: 'MenuBar' = None
    _bottom_panel: 'BottomPanel' = None
    _project_manager: 'ProjectManager' = None
    _editor_manager: 'EditorManager' = None

    _bottom_frame: 'tk.LabelFrame' = None
    _editor_frame: 'tk.Frame' = None
    
    # Singleton Pattern.
    # MainFrame should be static singleton whenever constructed, returned that same object, not constructed new one. 
    def __new__(cls: 'MainWindow', *args: tuple, **kwargs: dict) -> 'MainWindow':
        if MainWindow.__instance is None: 
            MainWindow.__instance = object.__new__(cls)
        return MainWindow.__instance

    # Construct window.
    def __init__(self: 'MainWindow', root: 'tk.Tk', config: 'Default', *args: tuple, **kwargs: dict) -> None:
        ttk.Frame.__init__(self, root, *args, **kwargs)

        self.pack(fill=tk.BOTH, expand=True)

        # Path to store information etc.
        def load_environment_config() -> None:
            Default(self).path: str = config.get("path")
            Default(self).darkmode: bool = config.get("darkmode")
            Default(self).font: str = config.get("font")
            
        # Center (x,y), window title, default widget style etc.
        def general_window_setup() -> None:
            TkHelper.configure_window(self._root, title="PyEnlightenmentCode")
            TkHelper.configure_visual(self._root, self.darkmode, "Text")
            TkHelper.configure_font(self._root, self.font)

        # Setup menubar
        def top_menu_bar_setup() -> 'MenuBar':
            self._menubar = MenuBar(root, MainWindow) #To-Do

        # Setup bottom panel with console view, terminal redirections, etc.
        def bottom_panel_setup() -> 'BottomPanel':
            self._bottom_frame = ttk.LabelFrame(self)
            TkHelper.configure_grid_x(self._bottom_frame, col=0, weight=1)
            TkHelper.configure_grid_y(self._bottom_frame, row=7, weight=1)
            self._bottompanel = BottomPanel(self._bottom_frame) #ToDo
            self._bottom_frame.pack(side = tk.BOTTOM, fill = tk.X, expand = False)

        # Left panel to navigate over files and methods
        def project_left_panel_setup() -> 'ProjectManager':
            #~ project_manager = ProjectManager() #ToDo
            pass
            
        # Load stored previously data
        def load_last_data() -> List['FileFrame']:
            #ToDo load last opened files.
            self._editor_frame = ttk.Frame(self)
            MainWindow._editor_manager = EditorManager(MainWindow, root, self._editor_frame) #ToDo
            self._editor_frame.pack(side = tk.TOP, fill = tk.BOTH, expand = True)

        self._root = root

        load_environment_config()
        general_window_setup()

        #Frames:
        bottom_panel_setup()
        top_menu_bar_setup()
        project_left_panel_setup()
        load_last_data()

        root.protocol("WM_DELETE_WINDOW", lambda: MainWindow.exit_(self._root))

    @staticmethod
    def add_to_mainloop(root: 'tk.Tk', time: int = 100, func: Callable = None) -> None:
        func()
        root.after(time, lambda: MainWindow.add_to_mainloop(root, time, func))

    @classmethod
    def exit_(cls: 'MainWindow', root: 'tk.Tk') -> None:
        logging.debug("`MainWindow.exit` called")
        TkHelper.save_position(root)
        Default.save()
        root.destroy()
        sys.exit(0)

    @classmethod
    def new_file(cls: 'MainWindow') -> None:
        logging.debug("`MainWindow.new_file` called")
        logging.error(str(dir(cls._editor_manager)))
        cls._editor_manager.new_file()
        pass

    @classmethod
    def load_file(cls: 'MainWindow') -> None:
        logging.debug("`MainWindow.load_file` called")
        MainWindow._editor_manager.load_file()
        pass

    @classmethod
    def save_file(cls: 'MainWindow', as_new: bool = False) -> None:
        logging.debug("`MainWindow.save_file` called")
        MainWindow._editor_manager.save_file(as_new = as_new)

    @classmethod
    def configure_settings(cls: 'MainWindow') -> None:
        logging.debug("`MainWindow.configure_settings` called")
        pass

class MainFrameErrorCatcher():
    def __init__(self, func, subst, widget):
        self.func = func
        self.subst = subst
        self.widget = widget

    def __call__(self, *args):
        try:
            if self.subst:
                args = self.subst(*args)
            return self.func(*args)
        except Exception as ex:
            MainFrameErrorCatcher.general_undefined_error_logging(ex)
            
    @staticmethod
    def general_undefined_error_logging(ex):
        logging.error("{")
        logging.error("Undefined error occured.")
        logging.error(f"Type: {type(ex).__name__}")
        logging.error(f"Reason: {str(ex)}")
        error_in_file = ex.__traceback__.tb_frame.f_code.co_filename[:-3]
        error_in_line = ex.__traceback__.tb_lineno
        logging.error(f"In: {error_in_file} at line: {error_in_line}")
        error_stack_item = ex.__traceback__.tb_next
        while error_stack_item:
            error_in_file = error_stack_item.tb_frame.f_code.co_filename[:-3]
            error_in_line = error_stack_item.tb_lineno
            logging.error(f"During: {error_in_file} at line: {error_in_line}")
            error_stack_item = error_stack_item.tb_next
        logging.error("}")

def mainloop():
    configs: 'Default' = Default.load()
    if configs.get("darkmode", True):
        root: 'tk.Tk()' = ThemedTk(theme="black")
    else:
        root: 'tk.Tk()' = ThemedTk(theme="arc")
    tk.CallWrapper = MainFrameErrorCatcher
    mw: 'MainWindow' = MainWindow(root, config=configs)
    mw.pack(fill = tk.BOTH)
    root.mainloop()

def argparse_logging_settings():
    parser.add_argument("-q", "--quiet", help="set logging to ERROR (default)",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.ERROR)
    parser.add_argument("-i", "--info", help="set logging to INFO",
                        action="store_const", dest="loglevel",
                        const=logging.INFO, default=logging.ERROR)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.ERROR)
    parser.add_argument("--test", help="test editor what is going wrong",
                        dest="test", default=None)
    parser.add_argument("--path", help="file path to store logs",
                        action="store", dest="path", default=None)

def argparse_program_settings():
    pass #To-Do

def argparse_validate():
    args = parser.parse_args()
    return args

#Debugging calling
if __name__ == "__main__" and __debug__:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s - %(levelname)-8s %(message)s')
    mainloop()

#Binary calling
if __name__ == "__main__" and not __debug__:
    parser = ArgumentParser(description=MainWindow.__doc__)
    argparse_logging_settings()
    argparse_program_settings()

    args = argparse_validate()
    logging.basicConfig(level=args.loglevel,
                        format=' %(name)s - %(levelname)-8s %(message)s')
    mainloop()
