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
        self.pack(fill=tk.BOTH, expand=1)

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
            menubar = MenuBar(root, MainWindow) #To-Do
            return menubar

        # Setup bottom panel with console view, terminal redirections, etc.
        def bottom_panel_setup() -> Type['BottomPanel']:
            bottom_frame = tk.LabelFrame(root, padx=1, pady=1)
            bottom_frame.rowconfigure(0, weight=1)
            bottom_frame.columnconfigure(0, weight=1)
            bottompanel = BottomPanel(bottom_frame) #ToDo
            bottom_frame.pack(side = tk.BOTTOM, fill = tk.X, expand=True)
            return bottompanel

        # Left panel to navigate over files and methods
        def project_left_panel_setup() -> Type['ProjectManager']:
            project_manager = ProjectManager() #ToDo
            pass
            
        # Load stored previously data
        def load_last_data() -> List[Type['FileFrame']]:
            #~ file_frame = FileFrame() #ToDo
            pass

        self._root = root

        load_environment_config()
        general_window_setup()
        self._bottompanel = bottom_panel_setup()

        #Frames:
        self._menubar = top_menu_bar_setup()
        self._projectmanager = project_left_panel_setup()
        self._opened_files = load_last_data()
        
        root.protocol("WM_DELETE_WINDOW", lambda: MainWindow.exit_(self._root))

        def update():
            logging.debug("FOO")
            root.after(5000, update)
        root.after(1000, update)

    @classmethod
    def exit_(cls, root):
        logging.debug("`MainWindow.exit` called")
        TkHelper.save_position(root)
        Default.save()
        root.destroy()

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
    def configure_settings(cls) -> None:
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
