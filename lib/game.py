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
    playing = True
    while (playing != False):
      self.draw(screen)
      playing = self.handle_input(screen)
      self.update()

  def draw(self, screen):
    # screen.clear()
    self.level.draw(screen)
    screen.addstr(self.hero.y, self.hero.x, '@', color_pair(1))

  def handle_input(self, keyboard):
      key_in = keyboard.getkey()
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
      elif (key_in is "q"):
        return False

  def update(self):
    update = True

  def init_curses(self):
    curs_set(0)
    init_pair(1, COLOR_MAGENTA, COLOR_BLACK)

  def is_floor(self, x, y):
        return self.level.tiles[x][y].type is "floor" or self.level.tiles[x][y].type is "corridor"

