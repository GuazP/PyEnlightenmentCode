#!/usr/bin/python3

import subprocess
import os

run_command = lambda shell_string: subprocess.run(shell_string, shell=True, universal_newlines=True)

class Settings():
    pip_installer = "pip"
    packages =  ["ttkthemes==2.4.0", #Bibliography: https://readthedocs.org/projects/ttkthemes/downloads/pdf/latest/
                 "tkinter", #Any version compatybile
                 "regex", #Any version compatybile
                 "jsonlib-python3", #Any version compatybile
                 "typing", #Any version compatybile
                 "pyautogui"
                ]#...

    def run(self):
        for package in Settings.packages:
            run_command(f"{Settings.pip_installer} install {package}")
        
if __name__ == "__main__":
    Settings.run(run_command)
