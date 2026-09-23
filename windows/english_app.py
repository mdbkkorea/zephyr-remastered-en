"""Open the GUI without arguments, or the native CLI with an action/--help."""
import sys
if __name__ == '__main__':
    if sys.argv[1:] == ['--crossover-launcher-version']:
        print('1')
        raise SystemExit(0)
    if sys.argv[1:] == ['--launch-crossover']:
        from english_crossover import main
    elif len(sys.argv) > 1:
        from english_engine import main
    else:
        from english_gui import main
    main()
