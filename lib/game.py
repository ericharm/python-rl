from level import Level
from hero import Hero
from curses import *
import random

class Game:

  def __init__(self, config):
    self.config = config
    self.level = Level(config['level'])
    self.level.generate(config['level'])
    hero_start = self.config['hero']['start']
    self.hero = Hero(hero_start['x'], hero_start['y'])

  def run(self, screen):

    self.init_curses()
    key_in = ""
    while (key_in != "q"):
      # draw
      screen.clear()
      self.level.draw(screen)
      screen.addstr(self.hero.y, self.hero.x, '@', color_pair(1))

      # get input
      key_in = screen.getkey()
      x = self.hero.x
      y = self.hero.y
      if (key_in == "KEY_LEFT" and self.is_floor(x - 1, y)):
        self.hero.x -= 1
      elif (key_in == "KEY_RIGHT" and self.is_floor(x + 1, y)):
        self.hero.x += 1
      elif (key_in == "KEY_UP" and self.is_floor(x, y - 1)):
        self.hero.y -= 1
      elif (key_in == "KEY_DOWN" and self.is_floor(x, y + 1)):
        self.hero.y += 1

  def init_curses(self):
    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

  def is_floor(self, x, y):
        return self.level.tiles[x][y].type == "floor"


