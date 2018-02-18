from level import Level
from player import Player
from hud import Hud
from entity import Hero
import random

class Game:

  def __init__(self, config):
    self.config = config
    self.level = self.generate_first_level()
    self.current_level = 0
    self.levels = [self.level]
    hero_start = self.level.get_random_floor_tile()
    self.hero = Hero(hero_start.x, hero_start.y)
    self.player = Player(self)
    self.level.entities.append(self.hero)

  def draw(self, window, hud): # pragma: no cover
    self.level.draw(window)
    hud.draw(self.hero.inventory)

  def handle_input(self, keyboard):
      try:
        key_in = keyboard.getkey()
      except:
        key_in = "0"
      return self.player.handle_input(key_in)

  def update(self):
    self.level.update()

  # private
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

