#!/usr/bin/python3

import subprocess
import os

from argparse import ArgumentParser

run_command = lambda shell_string: subprocess.run(shell_string, shell=True, universal_newlines=True)

class Command():
    #Settings
    optimizer = " " if False else " -OO " #Set __debug__ flag to False statement instead of deafult True || asserts are removed from bytecode || docstrings removed from binary 
    exec_name = "PyEnlightenmentCode"
    py_version = "python3.6"
    compiler = f"{py_version}{optimizer}-m PyInstaller"
    main = "main_frame.py"
    flags = " ".join(iter([ "--onefile", #Make only one binary independent file, which include dependencies.
                            "--hidden-import=tkinter", #Make hidden import for tkinter (there is some issue with normal dependency with tkinter, there is a workaround) 
                            ]))
    dependencies = ["doc/:doc/"]
    added_data = "--add-data " + " --add-data ".join(iter(dependencies))
    running_flags = ["--quiet"]
    running_flags = "" + " ".join(iter(running_flags))

    @classmethod
    def clean_cache_files(cls):
        return "rm -rfv ./*.pyc && rm -rfv ./*__pycache__"

    @classmethod
    def make_binary(cls):
        return " ".join(iter([ f"{cls.compiler}",
                               f"{cls.main}",
                               f"{cls.flags}",
                               f"{cls.added_data}",
                               f"--name {cls.exec_name}"
                               ]))

    @classmethod
    def extract_and_cleanup(cls):
        return " ".join(iter([ f"cp -v",
                               f"dist/{cls.exec_name} ./",
                               f"&&",
                               f"chmod",
                               f"+x",
                               f"{cls.exec_name}", 
                               f"&&",
                               f"rm -rfv",
                               f"dist/",
                               f"build/",
                               f"{cls.exec_name}.spec"
                               ]))

    @classmethod
    def run_binary(cls):
        return " ".join(iter([ f"./{cls.exec_name}",
                               f"{cls.running_flags}"
                               ]))
    @classmethod
    def run_and_remove_binary(cls):
        return " ".join(iter([ f"./{cls.exec_name}",
                               f"{cls.running_flags}",
                               f";",
                               f"rm -rfv",
                               f"./{cls.exec_name}"
                               ]))
                                

def main(args):
    #Clean python cache
    run_command(Command.clean_cache_files())
    
    #Compile program with dependencies
    run_command(Command.make_binary())

    #Cleanup and extract binary
    run_command(Command.extract_and_cleanup())

    if args.run_and_delete:
        #Run if flag is set to True, and delete binary after quit of the program (For testing pruposes)
        run_command(Command.run_and_remove_binary())
    elif args.run:
        #Run if flag is set to True
        run_command(Command.run_binary())

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", "--run", dest="run",
                        default=False, action="store_true",
                        help="Run after compile")
    parser.add_argument("-d", "--delete-after-run", dest="run_and_delete",
                        default=False, action="store_true",
                        help="Run after compile and delete when program ended")

    args = parser.parse_args()
    main(args)
