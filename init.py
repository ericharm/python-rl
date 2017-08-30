from curses import *

def main(stdscr):

    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

    row = "++++++++++++++++"
    char = {"x": 4, "y": 4}
    key_in = ""

    while (key_in != "q"):
      # clear screen
      stdscr.clear()

      # draw level
      for y in range(0,10):
          stdscr.addstr(y, 0, row);

      # draw character
      stdscr.addstr(char['y'], char['x'], '@', color_pair(1))

      # get input
      key_in = stdscr.getkey()

      # process input
      if (key_in == "KEY_LEFT"):
          char['x'] -= 1
      if (key_in == "KEY_RIGHT"):
          char['x'] += 1
      if (key_in == "KEY_UP"):
          char['y'] -= 1
      if (key_in == "KEY_DOWN"):
          char['y'] += 1


wrapper(main)

