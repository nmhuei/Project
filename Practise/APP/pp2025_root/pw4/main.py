import curses

from pw4.output import OutputUI


def main():
    ui = OutputUI()
    curses.wrapper(ui.main)


if __name__ == "__main__":
    main()