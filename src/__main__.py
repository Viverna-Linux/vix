import sys    
import signal

if __name__ == '__main__':
    try:
        # Preliminary check to make sure that we have tomllib
        import tomllib
        if tomllib.loads("") is not None:
            from vix import main
            main()
    except ImportError as e:
        print("vix requires Python 3.11 or later to run!", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt as e:
        signum = getattr(e, "signum", signal.SIGINT)
        signal.signal(signum, signal.SIG_DFL)
        sys.stderr.write(f"\nExiting Vix due to signal: {signal.strsignal(signum)} ({signum})\n")
        sys.stderr.flush()
        # raise_signal(signum)
