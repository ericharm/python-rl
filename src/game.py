from level import Level
from entity import Hero
import curses
import random

class Game:

  def __init__(self, config):
    self.config = config
    self.level = self.generate_first_level()
    self.current_level = 0
    self.levels = [self.level]
    hero_start = self.level.get_random_floor_tile()
    self.hero = Hero(hero_start.x, hero_start.y)

  def run(self, screen):
    pads = self.config['windows']
    self.window = curses.newpad(pads['level']['height'], pads['level']['width'])
    self.hud = curses.newpad(pads['hud']['height'], pads['hud']['width'])

    playing = True
    while (playing != False):
      self.draw()
      playing = self.handle_input(screen)
      self.update()

  def draw(self):
    # draw level
    self.level.draw(curses, self.window)
    self.hero.draw(curses, self.window)
    pad = self.config['windows']['level']
    self.window.refresh(0, 0, pad['y'], pad['x'], curses.LINES - 1, curses.COLS - 1)
    # draw hud - there will be a hud class later
    self.draw_hud()

  def draw_hud(self):
    pad = self.config['windows']['hud']
    for x in range(0, pad['width'] - 1):
      for y in range(0, pad['height']):
        if (x is 0 or x is pad['width'] - 2 or y is 0 or y is pad['height'] - 1):
          self.hud.addstr(y, x, ".", curses.color_pair(6))
    self.hud.refresh(0, 0, pad['y'], pad['x'], curses.LINES - 1, curses.COLS - 1)

  def handle_input(self, keyboard):
      # once this gets long we will implement a Player object
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
        self.descend_stairs()
      elif (key_in is "<" and self.level.tiles[x][y].type is "stairs_up"):
        self.ascend_stairs()
      elif (key_in is "q"):
        return False

  def update(self):
    # this is where we will handle AI and zapgun projectiles
    update = True


  def descend_stairs(self): #
    self.current_level += 1
    if len(self.levels) <= self.current_level:
      level = self.generate_next_level()
      self.levels.append(level)
    self.level = self.levels[self.current_level]

  def ascend_stairs(self): #
    self.current_level -= 1
    self.level = self.levels[self.current_level]

  def generate_first_level(self): #
    return Level(self.config['level']).generate().with_stairs_down()

  def generate_next_level(self): #
    if self.current_level < (self.config['game']['levels'] - 1):
      return Level(self.config['level']).generate().with_stairs_up(self.hero).with_stairs_down()
    else:
      return Level(self.config['level']).generate().with_stairs_up(self.hero)

  def is_walkable(self, x, y): #
    if y >= self.level.height or x >= self.level.width:
      return False
    return self.level.tiles[x][y].walkable()

