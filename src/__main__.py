import sys

if __name__ == '__main__':
    try:
        # Preliminary check to make sure that we have tomllib
        import tomllib
        if tomllib.loads("") is not None:
            from vix import main
            main()
    except ImportError as ignored:
        print("vix requires Python 3.11 or later to run!", file=sys.stderr)
        sys.exit(1)
