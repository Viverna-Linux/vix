import sys
from subcommands import SubCommand
from subcommands.get import GetCommand
from subcommands.remove import RemoveCommand
from subcommands.sync import SyncCommand

SUBCOMMANDS: list[SubCommand] = []
if __name__ == "vix":
    SUBCOMMANDS.append(GetCommand())
    SUBCOMMANDS.append(RemoveCommand())
    SUBCOMMANDS.append(SyncCommand())

def main():
    print("Usage: vix [subcommand] ...")
    for cmd in SUBCOMMANDS:
        print(f"  {cmd.get_name()} - {cmd.get_desc()}", file=sys.stderr)