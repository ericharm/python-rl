import curses

from util import Color

class Hud:

  def __init__(self, config):
    self.config = config

  def draw(self, window, inventory):
    window.border('|', '|', '-', '-',
        curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
    self.print_items(window, inventory)
    #  window.refresh(0, 0, self.config['y'], self.config['x'], curses.LINES - 1, curses.COLS - 1)

  def print_items(self, window, inv):
    for i in range(0, len(inv)):
      item = inv[i]
      name_x = 1 if i % 2 is 0 else 40
      name_y = (i / 2) + 1
      q_x = 20 if name_x is 1 else 61
      q_y = name_y
      window.addstr(name_y, name_x, inv[i]["name"], Color.use('white'))
      window.addstr(q_y, q_x, str(inv[i]["quantity"]), Color.use('white'))

