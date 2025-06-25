from subcommands import SubCommand

class SyncCommand(SubCommand):
    def get_name(self) -> str:
        return "sync"
    def get_desc(self) -> str:
        return "Retrieves data relating to packages into the local system"
    
    def run(self, args):
        print("sync command called!")
