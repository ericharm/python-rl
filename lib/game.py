from level import Level
from curses import *
import random

class Game:

  def __init__(self, config):
    self.config = config
    self.level = Level(config['level'])
    self.level.generate(config['level'])

  def is_floor(self, x, y):
        return self.level.tiles[x][y].type == "floor"

  def run(self, screen):

    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

    char = self.config['hero']['start']

    key_in = ""

    while (key_in != "q"):
      # draw
      screen.clear()
      self.level.draw(screen)
      screen.addstr(char['y'], char['x'], '@', color_pair(1))

      # get input
      key_in = screen.getkey()
      x = char['x']
      y = char['y']
      if (key_in == "KEY_LEFT" and self.is_floor(x - 1, y)):
        char['x'] -= 1
      elif (key_in == "KEY_RIGHT" and self.is_floor(x + 1, y)):
        char['x'] += 1
      elif (key_in == "KEY_UP" and self.is_floor(x, y - 1)):
        char['y'] -= 1
      elif (key_in == "KEY_DOWN" and self.is_floor(x, y + 1)):
        char['y'] += 1

