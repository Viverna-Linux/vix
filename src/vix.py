import sys
from subcommands import SubCommand
from subcommands.get import GetCommand
from subcommands.remove import RemoveCommand
from subcommands.sync import SyncCommand
from subcommands.bootstrap import BootstrapCommand

SUBCOMMANDS: list[SubCommand] = []
if __name__ == "vix":
    SUBCOMMANDS.append(GetCommand())
    SUBCOMMANDS.append(RemoveCommand())
    SUBCOMMANDS.append(SyncCommand())
    SUBCOMMANDS.append(BootstrapCommand())

def main():
    if len(sys.argv) >= 2:
        for cmd in SUBCOMMANDS:
            if cmd.get_name() == sys.argv[1]:
                cmd.setup_usage()
                cmd.run(cmd.argparse.parse_args(sys.argv[2:]))
                sys.exit(0)
    print("usage: vix [subcommand] ...\n\nsubcommands:", file=sys.stderr)
    for cmd in SUBCOMMANDS:
        print(f"  {cmd.get_name()} - {cmd.get_desc()}", file=sys.stderr)
