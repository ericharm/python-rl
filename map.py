from curses import *
from level import Level

level_width = 30
level_height = 15

level = Level(level_width,level_height)

def add_floor_tile(char):
    tile = level.tiles[char['x']][char['y']]
    tile.set_type("floor")


def main(stdscr):

    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

    char = {"x": 4, "y": 4}
    target = level.tiles[20][12]
    key_in = ""

    while (key_in != "q"):
      # draw
      stdscr.clear()
      level.draw(stdscr)
      stdscr.addstr(char['y'], char['x'], '@', color_pair(1))

      # get input
      key_in = stdscr.getkey()
      if (key_in == "KEY_LEFT" and char['x'] > 0):
          char['x'] -= 1
      elif (key_in == "KEY_RIGHT" and char['x'] < level_width - 1):
          char['x'] += 1
      elif (key_in == "KEY_UP" and char['y'] > 0):
          char['y'] -= 1
      elif (key_in == "KEY_DOWN" and char['y'] < level_height - 1):
          char['y'] += 1

      # update
      add_floor_tile(char)


wrapper(main)

