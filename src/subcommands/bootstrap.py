import sys
from subcommands import SubCommand
from utils import confirm

class BootstrapCommand(SubCommand):
    def get_name(self) -> str:
        return "bootstrap"
    def get_desc(self) -> str:
        return "Bootstraps a Stage 3 Viverna Tarball"
    def setup_usage(self):
        pass

    def run(self, args):
        print("""\x1b[1mYou are about to bootstrap a Viverna system and compress it into a tarball

Bootstrapping means compiling a base image of the system from scratch.
Viverna will build in 3 stages, the final stage will be
what you extract to your root filesystem to use Viverna.
Depending on the speed of your system, this could take hours (on older systems, days!)
Only do this when constructing a new system for the first time
or if you are automating this process in a pipeline.
        \x1b[0m""")
        if not confirm("Proceed?"):
            sys.exit(0)
        
