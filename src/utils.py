import os
import sys
from dataclasses import dataclass
from typing import Any

class ProgressBar:
    def __init__(self, msg: str):
        self.msg: str = msg
        self.first_draw: bool = True
    def update_progress(self, progress: float):
        """Redraws the progress bar on the terminal, progress is a value from 0.0 to 1.0"""
        width = 80
        try:
            width = os.get_terminal_size().columns
        finally:
            pass
        if not self.first_draw:
            sys.stderr.write("\x1b[1A")
        else:
            self.first_draw = False
        pos = int(width*progress)
        final_msg = self.msg+(" "*width-len(self.msg))
        final_msg = "\x1b[47;30m"+final_msg[0:pos]+"\x1b[0m"+final_msg[pos:]
        print(final_msg,file=sys.stderr)

@dataclass
class SharedGlobal:
    """Used to allow global variables to be mutably modified across module scopes"""
    value: Any

def confirm(question: str) -> bool:
    return input(f"{question} (\x1b[1;32my\x1b[0;1m/\x1b[31mn\x1b[0m) ").lower() == "y"

PACKAGE_DATABASE = SharedGlobal("/var/db/vix")

def get_repo_path(package_path: str) -> str:
    return os.path.join(PACKAGE_DATABASE.value,package_path)
def get_repo_data(package_path: str) -> str:
    file = open(get_repo_path(package_path),"r", encoding="utf-8")
    data = file.read(-1)
    file.close()
    return data
