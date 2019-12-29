## MainFrame Tk namespace
import tkinter as tk
from tkinter import filedialog

## MainFrame typing namespace
import typing
from typing import Type
from typing import List
from typing import Callable

## MainFrame libraries used
import logging
import os

## MainFrame using
from components.file_frame import EditorManager
from components.menu_frame import MenuBar
from components.bottom_frame import BottomPanel
from components.project_frame import ProjectManager

## MainFrame defaults and helper
from defaults.tkhelper import Default, TkHelper

class MainWindow(tk.Frame):
    __instance: 'MainWindow' = None
    _root: 'tk.Frame' = None
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
    def __init__(self: 'MainWindow', root: 'tk.Tk', *args: tuple, **kwargs: dict) -> None:
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.pack(fill=tk.BOTH, expand=1)

        # Path to store information etc.
        def load_environment_config() -> None:
            config = Default.load()
            Default(self).path: str = config.get("path")
            Default(self).darkmode: bool = config.get("darkmode")
            Default(self).font: str = config.get("font")
            
        # Center (x,y), window title, default widget style etc.
        def general_window_setup() -> None:
            TkHelper.configure_window(self._root, title="PyEnlightenmentCode")
            TkHelper.configure_visual(self._root, self.darkmode, "Button", "Text", "Label", "Frame", "tk")
            TkHelper.configure_font(self._root, self.font)

        # Setup menubar
        def top_menu_bar_setup() -> 'MenuBar':
            self._menubar = MenuBar(root, MainWindow) #To-Do

        # Setup bottom panel with console view, terminal redirections, etc.
        def bottom_panel_setup() -> 'BottomPanel':
            self._bottom_frame = tk.LabelFrame(root, padx=1, pady=1)
            TkHelper.configure_grid_x(self._bottom_frame, col=0, weight=1)
            TkHelper.configure_grid_y(self._bottom_frame, row=2, weight=1)
            self._bottompanel = BottomPanel(self._bottom_frame) #ToDo
            self._bottom_frame.pack(side = tk.BOTTOM, fill = tk.X, expand=False)

        # Left panel to navigate over files and methods
        def project_left_panel_setup() -> 'ProjectManager':
            #~ project_manager = ProjectManager() #ToDo
            pass
            
        # Load stored previously data
        def load_last_data() -> List['FileFrame']:
            #ToDo load last opened files.
            self._editor_frame = tk.Frame(root, padx=0, pady=0)
            self._editor_manager = EditorManager(MainWindow, root, self._editor_frame) #ToDo
            TkHelper.configure_grid_x(self._editor_frame, col=10, weight=1)
            TkHelper.configure_grid_y(self._editor_frame, row=2, weight=1)
            self._editor_frame.pack(side = tk.BOTTOM, fill = tk.BOTH, expand=True)

        self._root = root

        load_environment_config()
        general_window_setup()

        #Frames:
        bottom_panel_setup()
        top_menu_bar_setup()
        project_left_panel_setup()
        load_last_data()
        
        root.protocol("WM_DELETE_WINDOW", lambda: MainWindow.exit_(self._root))

        #~ def update():
            #~ logging.debug("FOO")
            #~ root.after(1000, update)
        #~ root.after(1000, update)

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

    @classmethod
    def new_file(cls: 'MainWindow') -> None:
        logging.debug("`MainWindow.new_file` called")
        pass

    @classmethod
    def load_file(cls: 'MainWindow') -> None:
        logging.debug("`MainWindow.load_file` called")
        selected_file = filedialog.askopenfilename(initialdir = os.path.expanduser("~"), title = "Select file", filetypes = (("python files","*.py"), ("all files", "*.*")))
        print(selected_file)
        pass

    @classmethod
    def save_file(cls: 'MainWindow', as_new: bool = False) -> None:
        file_data: 'FileContent' = self._filesframe.get_actual()
        logging.debug("`MainWindow.save_file` called")
        if as_new or file_data.is_new():
            selected_file = filedialog.asksaveasfilename(initialdir = os.path.expanduser("~"),
                                                         title = "Select where to save file",
                                                         filetypes = (("python files", "*.py"), ("all files", "*.*")))
        pass
        
    @classmethod
    def configure_settings(cls: 'MainWindow') -> None:
        logging.debug("`MainWindow.configure_settings` called")
        pass

class MainFrameErrorCatcher():
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass

def mainloop():
    root = tk.Tk()
    MainWindow(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

if __name__ == "__main__" and __debug__:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(name)s - %(levelname)-8s %(message)s')
    mainloop()
