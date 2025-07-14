import os
import sys
import threading
import time
import pprint
import subprocess
from dataclasses import dataclass
from typing import Any

class ProgressBar:
    def __init__(self, msg: str, spinner: bool = False):
        self.msg: str = msg
        self.first_draw: bool = True
        self.spinner = spinner
        self.thread = threading.Thread(target=_do_spinner, args=(self,), daemon=True)
        self.run_spinner: bool = False
        self.spinner_index = 0
    def start_spinner(self):
        self.run_spinner = True
        self.thread.start()
    def stop_spinner(self):
        self.run_spinner = False
        self.thread.join()
    def update_progress(self, progress: float):
        """Redraws the progress bar on the terminal, progress is a value from 0.0 to 1.0"""
        width = 80
        try:
            width = os.get_terminal_size().columns
        finally:
            pass
        if not self.first_draw:
            sys.stderr.write("\x1b[1A\r")
        else:
            self.first_draw = False
        pos = int(width*progress)
        spinner_syms = ["/","-","\\","|"]
        sys.stderr.write(f"\x1b]2;{self.msg}\x07")
        m = self.msg+" | "+((str(int(round(progress,2)*100))+"%") if not self.spinner else "["+spinner_syms[self.spinner_index]+"]")
        final_msg = m+" "*(width-len(m))
        final_msg = "\x1b[1;47;30m"+final_msg[0:pos]+"\x1b[0;1m"+final_msg[pos:]+"\x1b[0m"
        print(final_msg,file=sys.stderr)
def _do_spinner(pbar: ProgressBar):
    while pbar.run_spinner:
        pbar.spinner_index = (pbar.spinner_index + 1) % 4
        pbar.update_progress(0)
        time.sleep(0.25)
    pbar.update_progress(1)
def post_status(msg: str):
    sys.stderr.write(f"\x1b]2;{msg}\x07")
    print("\x1b[0;1m"+msg+"\x1b[0m", file=sys.stderr)

@dataclass
class SharedGlobal:
    """Used to allow global variables to be mutably modified across module scopes"""
    value: Any

def confirm(question: str) -> bool:
    return input(f"{question} (\x1b[1;32my\x1b[0;1m/\x1b[31mn\x1b[0m) ").lower() == "y"

PACKAGE_DATABASE = SharedGlobal("/var/db/vix/pkgrepo")
TARGET_TRIPLET = subprocess.run("gcc -dumpmachine", capture_output=True, shell=True,executable="/bin/bash").stdout.decode("utf-8").splitlines()[0]
CROSS_TARGET_TRIPLET = ""
if TARGET_TRIPLET is not None:
    split = TARGET_TRIPLET.split("-")
    CROSS_TARGET_TRIPLET = split[0]+"-viverna-linux-gnu"
SYSTEM_ROOT = SharedGlobal("/")

def get_repo_path(package_path: str) -> str:
    return os.path.join(PACKAGE_DATABASE.value,package_path)
def get_repo_data(package_path: str) -> str:
    file = open(get_repo_path(package_path),"r", encoding="utf-8")
    data = file.read(-1)
    file.close()
    return data
def setup_env(vars: dict[str, Any]) -> str:
    res = """fail() {
    echo "Vix: Something broke!" > /dev/stderr
    exit 1
}

"""
    for key, val in vars.items():
        res = res + key + "=" + pprint.saferepr(val) + "\n"
    res = res + "PATH=$ROOT/tools/bin:$PATH\n"
    return res
    
