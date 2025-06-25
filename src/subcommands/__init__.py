from argparse import ArgumentParser, Namespace

class SubCommand:
    def __init__(self):
        self.argparse: ArgumentParser = ArgumentParser(prog="vix "+self.get_name(),
                                                       description=self.get_desc())

    def get_name(self) -> str:
        """Retrieves the name of the subcommand"""
        return "placeholder"
    def get_desc(self) -> str:
        """Retrieves the description of the subcommand"""
        return "placeholder"

    def setup_usage(self):
        """Sets up the ArgumentParser for run"""

    def run(self, args: Namespace):
        """Runs the subcommand with parsed arguments being passed to it"""
