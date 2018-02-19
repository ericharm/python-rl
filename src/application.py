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
      state.draw(self.main_window, self.footer_window)
      window_config = self.config['windows']['body']
      footer_config = self.config['windows']['footer']
      self.main_window.refresh(0, 0, window_config['y'], window_config['x'],
          curses.LINES - 1, curses.COLS - 1)
      self.footer_window.refresh(0, 0, footer_config['y'], footer_config['x'],
          curses.LINES - 1, curses.COLS - 1)

  def handle_input(self, keyboard):
    try:
      key_in = keyboard.getkey()
    except:
      key_in = "0"
    return self.states[-1].handle_input(key_in)

  def create_windows(self, window_configs):
    body_setup = window_configs['body']
    footer_setup = window_configs['footer']
    self.main_window = curses.newpad(body_setup['height'], body_setup['width'])
    self.footer_window = curses.newpad(footer_setup['height'], footer_setup['width'])

  def set_title_screen(self):
    title = Title(self.config, self.states)
    self.states.append(title)

