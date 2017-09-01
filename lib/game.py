from level import Level
from curses import *

class Game:

    def __init__(self, config):
        self.LEVEL_WIDTH = config['level']['width']
        self.LEVEL_HEIGHT = config['level']['height']
        self.level = Level(self.LEVEL_WIDTH, self.LEVEL_HEIGHT)

    def set_tile_type_at_char(self, char, type):
        tile = self.level.tiles[char['x']][char['y']]
        tile.set_type(type)

    def run(self, screen):

        curs_set(0)
        init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

        char = {"x": 4, "y": 4}
        target = self.level.tiles[20][12]

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
          elif (key_in == "KEY_RIGHT" and char['x'] < self.LEVEL_WIDTH - 1):
              char['x'] += 1
          elif (key_in == "KEY_UP" and char['y'] > 0):
              char['y'] -= 1
          elif (key_in == "KEY_DOWN" and char['y'] < self.LEVEL_HEIGHT - 1):
              char['y'] += 1

          # update
          self.set_tile_type_at_char(char, "floor")

