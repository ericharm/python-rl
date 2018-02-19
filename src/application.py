from game import Game
from title import Title
from hud import Hud
import curses

class Application: # pragma: no cover

  def __init__(self, config):
    self.config = config
    self.states = []

  def run(self, screen):
    self.create_windows(self.config['windows'])
    self.set_title_screen()
    playing = True
    while (playing != False):
      self.draw()
      playing = self.handle_input(screen)
      self.states[-1].update()

  def draw(self):
    for state in self.states:
      state.draw(self.window, self.hud)
      window_config = self.config['windows']['game']
      self.window.refresh(0, 0, window_config['y'], window_config['x'],
          curses.LINES - 1, curses.COLS - 1)

  def handle_input(self, keyboard):
    try:
      key_in = keyboard.getkey()
    except:
      key_in = "0"
    return self.states[-1].handle_input(key_in)

  def create_windows(self, window_configs):
    game_win_setup = window_configs['game']
    hud_win_setup = window_configs['hud']
    self.window = curses.newpad(game_win_setup['height'], game_win_setup['width'])
    hud_pad = curses.newpad(hud_win_setup['height'], hud_win_setup['width'])
    self.hud = Hud(hud_pad, self.config['windows']['hud'])

  def set_title_screen(self):
    title = Title(self.config, self.states)
    self.states.append(title)

