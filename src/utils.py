import os
from dataclasses import dataclass
from typing import Any

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
