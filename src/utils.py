
def confirm(question: str) -> bool:
    return input(f"{question} (\x1b[1;32my\x1b[0;1m/\x1b[31mn\x1b[0m) ").lower() == "y"