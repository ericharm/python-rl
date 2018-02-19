from level import Level
from game_input_controller import GameInputController
from entity import Hero
from util import Color
import curses
import random

class Game:

  def __init__(self, config, state_stack):
    self.config = config
    self.level = self.generate_first_level()
    self.current_level = 0
    self.levels = [self.level]
    hero_start = self.level.get_random_floor_tile()
    self.hero = Hero(hero_start.x, hero_start.y)
    self.player = GameInputController(self)
    self.level.entities.append(self.hero)

  def draw(self, windows): # pragma: no cover
    self.display_heading(windows['head'])
    self.level.draw(windows['body'])
    self.draw_hud(windows['footer'])

  def handle_input(self, key):
    return self.player.handle_input(key)

  def update(self):
    self.level.update()

  def display_heading(self, window): # pragma: no cover
    window.clear()
    window.border('|', '|', '-', '-',
        curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
    title = 'Level ' + str(self.current_level)
    window.addstr(1, 10, title, Color.use('yellow'))

  def draw_hud(self, window): #pragma: no cover
    window.border('|', '|', '-', '-',
        curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
    self.print_inventory(window, self.hero.inventory)

  def print_inventory(self, window,inv): #pragma: no cover
    for i in range(0, len(inv)):
      name_x = 1 if i % 2 is 0 else 40
      name_y = (i / 2) + 1
      q_x = 20 if name_x is 1 else 61
      q_y = name_y
      window.addstr(name_y, name_x, inv[i]["name"], Color.use('white'))
      window.addstr(q_y, q_x, str(inv[i]["quantity"]), Color.use('white'))

  def generate_first_level(self):
    return Level(self.config['level']).generate().with_stairs_down()

  def generate_next_level(self):
    if self.current_level < (self.config['game']['levels'] - 1):
      return Level(self.config['level']).generate().with_stairs_up(self.hero).with_stairs_down()
    else:
      return Level(self.config['level']).generate().with_stairs_up(self.hero)

  def descend_stairs(self):
    self.current_level += 1
    if len(self.levels) <= self.current_level:
      level = self.generate_next_level()
      self.levels.append(level)
    self.reset_hero_level()

  def ascend_stairs(self):
    self.current_level -= 1
    self.reset_hero_level()

  def reset_hero_level(self):
    self.level.entities.remove(self.hero)
    self.level = self.levels[self.current_level]
    self.level.entities.append(self.hero)

