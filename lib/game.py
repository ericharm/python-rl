from level import Level
from hero import Hero
import curses
import random

class Game:

  def __init__(self, config):
    self.config = config

    self.levels = []
    self.level = Level(config['level'])
    self.level.generate(config['level'])
    self.levels.append(self.level)

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
    screen.addstr(self.hero.y, self.hero.x, '@', curses.color_pair(5))

  def handle_input(self, keyboard):
      key_in = keyboard.getkey()
      x = self.hero.x
      y = self.hero.y
      if   (key_in == "KEY_LEFT" and self.is_walkable(x - 1, y)):
        self.hero.x -= 1
      elif (key_in == "KEY_RIGHT" and self.is_walkable(x + 1, y)):
        self.hero.x += 1
      elif (key_in == "KEY_UP" and self.is_walkable(x, y - 1)):
        self.hero.y -= 1
      elif (key_in == "KEY_DOWN" and self.is_walkable(x, y + 1)):
        self.hero.y += 1
      elif (key_in is ">" and self.level.tiles[x][y].type is "stairs_down"):
        self.generate_new_level()
      elif (key_in is "q"):
        return False

  def update(self):
    update = True

  def init_curses(self):
    curses.curs_set(0)
    # empty
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    # stairs_down
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # corridor
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # floor
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    # hero char
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)


  def generate_new_level(self):
    self.level = Level(self.config['level'])
    self.level.generate(self.config['level'])

  def is_walkable(self, x, y):
    if y >= self.level.height or x >= self.level.width:
      return False
    return self.level.tiles[x][y].walkable()

