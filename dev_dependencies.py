#!/usr/bin/python3

import subprocess
import os

run_command = lambda shell_string: subprocess.run(shell_string, shell=True, universal_newlines=True)

class Settings():
    pip_installer = "pip"
    packages =  ["ttkthemes==2.4.0", #Bibliography: https://readthedocs.org/projects/ttkthemes/downloads/pdf/latest/
                 "tkinter"#,
                 ]#...

if __name__ == "__main__":
    Settings.run(run_command)
