from subcommands import SubCommand

class BootstrapCommand(SubCommand):
    def get_name(self) -> str:
        return "bootstrap"
    def get_desc(self) -> str:
        return "Bootstraps a Stage 3 Viverna Tarball"
    def setup_usage(self):
        pass

    def run(self, args):
        pass
