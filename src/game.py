from level import Level
from game_input_controller import GameInputController
from entity import Hero
from util import Color
from hud import Hud
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
    self.hud = Hud(self.config['windows']['footer'])
    self.level.entities.append(self.hero)

  def draw(self, windows): # pragma: no cover
    self.display_heading(windows['head'])
    self.level.draw(windows['body'])
    self.hud.draw(windows['footer'], self.hero.inventory)

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

