import sys
import tomllib
import tempfile
import os
from subcommands import SubCommand
from utils import confirm, PACKAGE_DATABASE, SYSTEM_ROOT, get_repo_data
from package import PackageGet

class BootstrapCommand(SubCommand):
    def get_name(self) -> str:
        return "bootstrap"
    def get_desc(self) -> str:
        return "Bootstraps a Stage 3 Viverna Tarball"
    def setup_usage(self):
        self.argparse.add_argument("--repo", help="Specifies a different local clone of a package repository (FOR TESTING ONLY!)")

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
        if args.repo is not None:
            PACKAGE_DATABASE.value = args.repo
        stage1 = os.path.join(tempfile.gettempdir(),"stage1")
        os.makedirs(stage1, exist_ok=True)
        SYSTEM_ROOT.value = stage1
        bootstrap = tomllib.loads(get_repo_data("bootstrap.toml"))
        for pkg in bootstrap["packages"]["stage1"]:
            pkgver = pkg.split(" ")
            PackageGet(pkgver[0],pkgver[1]).build()
