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

  def run(self, screen):
    self.create_windows(self.config['windows'])
    self.player = Player(self)
    playing = True
    while (playing != False):
      self.draw()
      playing = self.handle_input(screen)
      self.update()

  def draw(self):
    self.level.draw(curses, self.window)
    # this step will later draw an array of entities
    self.hero.draw(curses, self.window)
    self.hud.draw(curses, self.hero.inventory)
    window_config = self.config['windows']['game']
    self.window.refresh(0, 0, window_config['y'], window_config['x'],
                        curses.LINES - 1, curses.COLS - 1)

  def handle_input(self, keyboard):
      # once this gets long we will implement a Player object
      try:
        key_in = keyboard.getkey()
      except:
        key_in = "0"
      return self.player.handle_input(key_in)


  def update(self):
    # this is where we will handle AI and zapgun projectiles
    update = True


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

