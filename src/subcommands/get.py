from subcommands import SubCommand

class GetCommand(SubCommand):
    def get_name(self) -> str:
        return "get"
    def get_desc(self) -> str:
        return "Retrives and builds packages, used to install new packages, or update existing ones"
    
    def setup_usage(self):
        self.argparse.add_argument("-y", action="store_true", help="Automatically puts \"y\" on any y/n prompt")
        self.argparse.add_argument("-u", "--update", action="store_true", help="Updates the specified package(s)")
        self.argparse.add_argument("-r", "--rebuild", action="store_true", help="Rebuild existing package(s)")
        self.argparse.add_argument("-p", "--pretend", action="store_true", help="Simulates a \"vix get\" operation without performing it")

        self.argparse.add_argument("packages", nargs="+", help="The packages to get")

    def run(self, args):
        print("get command called!")