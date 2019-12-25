## MainFrame libraries
import tkinter as tk
import pickle
import typing
from typing import Type
from typing import List
import logging

## MainFrame using
from components.file_frame import FileFrame
from components.menu_frame import MenuBar
from components.bottom_frame import BottomPanel
from components.project_frame import ProjectManager

## MainFrame defaults
from defaults.main_frame import Default

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
            config = None ## Pickled data loading
            Default(self).path: str = config
            #~ print(self.path)

        # Center (x,y), window title, etc.
        def general_window_setup() -> None:
            pass

        # Setup menubar
        def top_menu_bar_setup() -> Type['MenuBar']:
            #~ menubar = MenuBar() #ToDo
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

    def __exit__(self) -> None:
        def save_existing_data():
            pass

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
