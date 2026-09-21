"""Open the GUI without arguments, or the native CLI with an action/--help."""
import sys
if __name__ == '__main__':
    if len(sys.argv) > 1:
        from english_engine import main
    else:
        from english_gui import main
    main()
