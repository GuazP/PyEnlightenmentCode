#!/usr/bin/python3

from argparse import ArgumentParser
import logging

from main_frame import MainWindow
from main_frame import mainloop

def main():
    #~ if args.debug:
        #~ pass

    #~ elif args.install:
        #~ pass
    mainloop()

def argparse_logging_settings():
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.ERROR)
    parser.add_argument("-i", "--info", help="set logging to INFO",
                        action="store_const", dest="loglevel",
                        const=logging.INFO, default=logging.ERROR)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.ERROR)

def argparse_program_settings():
    pass

def argparse_validate():
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    parser = ArgumentParser(description=MainWindow.__doc__)
    argparse_logging_settings()
    argparse_program_settings()

    args = argparse_validate()
    logging.basicConfig(level=args.loglevel,
                        format=' %(name)s - %(levelname)-8s %(message)s')

    mainloop()
