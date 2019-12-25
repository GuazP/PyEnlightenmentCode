import os
import logging

class Default():
    """Default config for MainFrame object, to separate code"""
    def __init__(self, parent):
        super().__setattr__('parent', parent)

    def __getattr__(self, attr):
        return getattr(self.parent, attr)

    def __setattr__(self, attr, value):
        if value is None:
            logging.debug(f"Can't load `{attr}`. Loading default `{attr}` as `{self.defaults.get(attr, None)}`.")
            self.parent.__setattr__(attr, self.defaults.get(attr, None))
        else:
            logging.debug(f"Loading `{attr}` as `{value}`")
            self.parent.__setattr__(attr, value)

    home_loc = os.path.expanduser("~")
    defaults = {"path": os.path.join(home_loc, ".config", "PyEnlightenmentCode")}

