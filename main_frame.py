## MainFrame libraries
import tkinter as tk
import typing
from typing import Type
from typing import List
import logging
import re

## MainFrame using
from components.file_frame import FileFrame
from components.menu_frame import MenuBar
from components.bottom_frame import BottomPanel
from components.project_frame import ProjectManager

## MainFrame defaults
from defaults.tkhelper import Default

## TkSettingsHelper
from defaults.tkhelper import TkHelper

class MainWindow(tk.Frame):
    __instance: 'MainWindow' = None
    _root: 'tk.Frame' = None
    _menubar: 'MenuBar' = None
    _bottompanel: 'BottomPanel' = None
    _projectmanager: 'ProjectManager' = None
    
    # Singleton Pattern.
    # MainFrame should be static singleton whenever constructed, returned that same object, not constructed new one. 
    def __new__(cls, *args, **kwargs) -> Type['MainWindow']:
        if MainWindow.__instance is None: 
            MainWindow.__instance = object.__new__(cls)
        return MainWindow.__instance

    # Construct window.
    def __init__(self, root: Type['tk.Tk'], *args: tuple, **kwargs: dict) -> None:
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Path to store information etc.
        def load_environment_config() -> None:
            config = Default.load()
            Default(self).path: str = config.get("path")
            Default(self).darkmode: bool = config.get("darkmode")
            
        # Center (x,y), window title, default widget style etc.
        def general_window_setup() -> None:
            TkHelper.configure_window(self._root, title="PyEnlightenmentCode")
            TkHelper.configure_visual(self._root, self.darkmode, "Button", "Text", "Label")

        # Setup menubar
        def top_menu_bar_setup() -> Type['MenuBar']:
            _menubar = MenuBar(root, MainWindow) #To-Do
            pass

        # Setup bottom panel with console view, terminal redirections, etc.
        def bottom_panel_setup() -> Type['BottomPanel']:
            #~ bottom_panel = BottomPanel() #ToDo
            pass

        # Left panel to navigate over files and methods
        def project_left_panel_setup() -> Type['ProjectManager']:
            #~ project_manager = ProjectManager() #ToDo
            pass
            
        # Load stored previously data
        def load_last_data() -> List[Type['FileFrame']]:
            #~ file_frame = FileFrame() #ToDo
            pass

        self._root = root

        load_environment_config()
        general_window_setup()

        #Frames:
        self._menubar = top_menu_bar_setup()
        self._bottompanel = bottom_panel_setup()
        self._projectmanager = project_left_panel_setup()
        self._opened_files = load_last_data()
        
        tk.Button(self._root, text="KUPA").pack()

    @classmethod
    def exit_(cls, root):
        logging.debug("`MainWindow.exit` called")
        TkHelper.save_position(root)
        Default.save()

    @classmethod
    def new_file(cls):
        logging.debug("`MainWindow.new_file` called")
        pass

    @classmethod
    def load_file(cls):
        logging.debug("`MainWindow.load_file` called")
        pass

    @classmethod
    def save_file(cls, as_new: bool=False) -> None:
        logging.debug("`MainWindow.save_file` called")
        pass
        
    @classmethod
    def configure_settings(cls, as_new: bool=False) -> None:
        logging.debug("`MainWindow.save_file` called")
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
                        format=' %(name)s - %(levelname)-8s %(message)s')
    mainloop()
