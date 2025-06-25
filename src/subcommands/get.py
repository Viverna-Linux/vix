from subcommands import SubCommand

class GetCommand(SubCommand):
    def get_name(self) -> str:
        return "get"
    def get_desc(self) -> str:
        return "Retrives and builds packages, used to install new packages, or update existing ones"
    
    def run(self, args: list[str], flags: list[str]):
        print("get command called!")
