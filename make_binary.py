# /usr/bin/python3

import subprocess
import os

from argparse import ArgumentParser

run_command = lambda shell_string: subprocess.run(shell_string, shell=True, universal_newlines=True)

class Command():
    #Settings
    exec_name = "PyEnlightenmentCode"
    compiler = "pyinstaller"
    main = "__main__.py"
    flags = " ".join(iter(["--onefile"]))
    dependencies = ["doc/"]
    added_data = "--add-data" + "--add-data".join(iter(dependencies))

    @classmethod
    def get(cls):
        return f" ".join(iter(["{cls.compiler}",
                               "{cls.main}",
                               "{cls.flags}",
                               "{cls.added_data}",
                               "-o {cls.exec_name}"
                              ])

def main(args):
    #Compile program with dependencies
    run_command(repr(Command.get()))

    #Cleanup and extract binary

    #Run if flag is set to True
    if args.run:
        #~ run_command()
        pass

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", "--run", dest="run",
                        default=False, store=True,
                        help="Run after compile")
                        
    args = parser.parse_args()
    main(args)
