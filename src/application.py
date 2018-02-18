from game import Game
from hud import Hud
import curses

class Application: # pragma: no cover

  def __init__(self, config):
    self.config = config
    self.create_windows(self.config['windows'])
    game = Game(self.config)
    self.states = [game]

  def run(self, screen):
    self.game = Game(self.config)
    playing = True
    while (playing != False):
      self.draw()
      playing = self.states[-1].handle_input(screen)
      self.states[-1].update()

  def create_windows(self, window_configs):
    game_win_setup = window_configs['game']
    hud_win_setup = window_configs['hud']
    self.window = curses.newpad(game_win_setup['height'], game_win_setup['width'])
    hud_pad = curses.newpad(hud_win_setup['height'], hud_win_setup['width'])
    self.hud = Hud(hud_pad, self.config['windows']['hud'])

  def draw(self):
    self.states[-1].draw(self.window, self.hud)
    window_config = self.config['windows']['game']
    self.window.refresh(0, 0, window_config['y'], window_config['x'],
                        curses.LINES - 1, curses.COLS - 1)

