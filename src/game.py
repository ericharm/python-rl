from level import Level
from game_input_controller import GameInputController
from entity import Hero
from hud import Hud
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

  def draw(self, window, footer): # pragma: no cover
    self.level.draw(window)
    self.hud.draw(footer, self.hero.inventory)

  def handle_input(self, key):
    return self.player.handle_input(key)

  def update(self):
    self.level.update()

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

