from subcommands import SubCommand

class RemoveCommand(SubCommand):
    def get_name(self) -> str:
        return "remove"
    def get_desc(self) -> str:
        return "Removes existing packages and (optionally) their dependencies"
    
    def run(self, args):
        print("remove command called!")
