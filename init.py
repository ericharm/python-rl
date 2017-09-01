from curses import *
import yaml
from lib.level import Level

with open("config/config.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)


LEVEL_WIDTH = config['level']['width']
LEVEL_HEIGHT = config['level']['height']

level = Level(LEVEL_WIDTH,LEVEL_HEIGHT)

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
      elif (key_in == "KEY_RIGHT" and char['x'] < LEVEL_WIDTH - 1):
          char['x'] += 1
      elif (key_in == "KEY_UP" and char['y'] > 0):
          char['y'] -= 1
      elif (key_in == "KEY_DOWN" and char['y'] < LEVEL_HEIGHT - 1):
          char['y'] += 1

      # update
      add_floor_tile(char)


wrapper(main)

