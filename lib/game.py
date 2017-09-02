from level import Level
from curses import *
import random

class Game:

  def __init__(self, config):
    self.width = config['level']['width']
    self.height = config['level']['height']
    self.level = Level(self.width, self.height)
    self.config = config

  def set_tile_type_at_char(self, char, type):
    tile = self.level.tiles[char['x']][char['y']]
    tile.set_type(type)

  def is_floor(self, x, y):
    return self.level.tiles[x][y].type == "floor"

  def build_map(self, screen, char):
    # target = self.config['map']['target']
    # direction = ""
    # self.level.add_room(3, 1, 5, 3)
    for attempt in range(0,10):
      odd_x = 1 + (random.randint(0, self.level.width / 2) * 2)
      odd_y = 1 + (random.randint(0, self.level.height / 2) * 2)

      # odd_x = 1 + (random.randint(0, 50) * 2)
      # odd_y = 1 + (random.randint(0, 25) * 2)

      rooms = self.config['map']['rooms']
      odd_width = 1 + (random.randint(0, rooms['max_width'] / 2) * 2)
      odd_height = 1 + (random.randint(0, rooms['max_height'] / 2) * 2)

      self.level.add_room(odd_x, odd_y, odd_width, odd_height)
    # while (char["x"] != target["x"] and char["y"] != target["y"]):
      # direction = random.sample(["n","s","e", "e", "w", "w"], 1)[0]

      # get input
      # if (direction == "w" and char['x'] > 0):
        # char['x'] -= 1
      # elif (direction == "e" and char['x'] < self.width - 1):
        # char['x'] += 1
      # elif (direction == "n" and char['y'] > 0):
        # char['y'] -= 1
      # elif (direction == "s" and char['y'] < self.height - 1):
        # char['y'] += 1

      # update
      # self.set_tile_type_at_char(char, "floor")

  def run(self, screen):

    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

    char = self.config['hero']['start']
    self.build_map(screen, char)

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

      # update
      self.set_tile_type_at_char(char, "floor")

