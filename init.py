import curses
from yaml import load, CLoader, YAMLError
from src.application import Application

with open("config/config.yml", "r") as stream:
    try:
        config = load(stream, CLoader)
    except YAMLError as exc:
        print(exc)


def main(stdscr):
    application = Application(config)
    application.run(stdscr)


def init_curses():
    curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.noecho()
    curses.cbreak()


init_curses()
curses.wrapper(main)
