from level import Level
from player import Player
from hud import Hud
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
    # self.level.tiles[hero_start.x][hero_start.y].entities.append(self.hero)
    self.level.entities.append(self.hero)

  def run(self, screen):
    self.create_windows(self.config['windows'])
    self.player = Player(self)
    playing = True
    while (playing != False):
      self.draw()
      playing = self.handle_input(screen)
      self.update()

  def draw(self):
    # draw level, its tiles, their entities
    self.level.draw(curses, self.window)
    # draw hud
    self.hud.draw(curses, self.hero.inventory)
    window_config = self.config['windows']['game']
    self.window.refresh(0, 0, window_config['y'], window_config['x'],
                        curses.LINES - 1, curses.COLS - 1)

  def handle_input(self, keyboard):
      try:
        key_in = keyboard.getkey()
      except:
        key_in = "0"
      return self.player.handle_input(key_in)


  def update(self):
    self.level.update()

  # private

  def create_windows(self, window_configs):
    game_win_setup = window_configs['game']
    hud_win_setup = window_configs['hud']
    self.window = curses.newpad(game_win_setup['height'], game_win_setup['width'])
    hud_pad = curses.newpad(hud_win_setup['height'], hud_win_setup['width'])
    self.hud = Hud(hud_pad, self.config['windows']['hud'])

  def generate_first_level(self): #
    return Level(self.config['level']).generate().with_stairs_down()

  def generate_next_level(self): #
    if self.current_level < (self.config['game']['levels'] - 1):
      return Level(self.config['level']).generate().with_stairs_up(self.hero).with_stairs_down()
    else:
      return Level(self.config['level']).generate().with_stairs_up(self.hero)

  def descend_stairs(self): #
    self.current_level += 1
    if len(self.levels) <= self.current_level:
      level = self.generate_next_level()
      self.levels.append(level)
    self.level.entities.remove(self.hero)
    self.level = self.levels[self.current_level]
    self.level.entities.append(self.hero)
    self.level.tiles[self.hero.x][self.hero.y].entities.append(self.hero)

  def ascend_stairs(self): #
    self.current_level -= 1
    self.level = self.levels[self.current_level]

  def is_walkable(self, x, y): #
    if y >= self.level.height or x >= self.level.width:
      return False
    return self.level.tiles[x][y].walkable()

