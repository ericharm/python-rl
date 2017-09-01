from level import Level
from curses import *

class Game:

  def __init__(self, config):
    self.width = config['level']['width']
    self.height = config['level']['height']
    self.level = Level(self.width, self.height)

  def set_tile_type_at_char(self, char, type):
    tile = self.level.tiles[char['x']][char['y']]
    tile.set_type(type)

  def run(self, screen):

    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

    char = {"x": 4, "y": 4}
    target = {"x": 20, "y": 12}

    direction = ""

    while (char["x"] != target["x"] and char["y"] != target["y"]):
      direction = random.sample(["n","s","e","w"], 1)[0]

      # draw
      screen.clear()
      self.level.draw(screen)
      screen.addstr(char['y'], char['x'], '@', color_pair(1))

      # get input
      if (direction == "KEY_LEFT" and char['x'] > 0):
        char['x'] -= 1
      elif (direction == "KEY_RIGHT" and char['x'] < self.width - 1):
        char['x'] += 1
      elif (direction == "KEY_UP" and char['y'] > 0):
        char['y'] -= 1
      elif (direction == "KEY_DOWN" and char['y'] < self.height - 1):
        char['y'] += 1

      # update
      self.set_tile_type_at_char(char, "floor")

    key_in = ""

    while (key_in != "q"):
      # draw
      screen.clear()
      self.level.draw(screen)
      screen.addstr(char['y'], char['x'], '@', color_pair(1))

      # get input
      key_in = screen.getkey()
      if (key_in == "KEY_LEFT" and char['x'] > 0):
        char['x'] -= 1
      elif (key_in == "KEY_RIGHT" and char['x'] < self.width - 1):
        char['x'] += 1
      elif (key_in == "KEY_UP" and char['y'] > 0):
        char['y'] -= 1
      elif (key_in == "KEY_DOWN" and char['y'] < self.height - 1):
        char['y'] += 1

      # update
      self.set_tile_type_at_char(char, "floor")

