class Hud:

  def __init__(self, window, config):
    self.window = window
    self.config = config

  def draw(self, curses, inventory):
    self.outline(curses)
    self.print_items(curses, inventory)
    self.window.refresh(0, 0, self.config['y'], self.config['x'], curses.LINES - 1, curses.COLS - 1)

  def print_items(self, curses, inv):
      for i in range(0, len(inv)):
        item = inv[i]
        name_x = 1 if i % 2 is 0 else 40
        name_y = (i / 2) + 1
        q_x = 20 if name_x is 1 else 61
        q_y = name_y
        self.window.addstr(name_y, name_x, inv[i]["name"], curses.color_pair(6))
        self.window.addstr(q_y, q_x, str(inv[i]["quantity"]), curses.color_pair(6))

  def outline(self, curses):
    for x in range(0, self.config['width'] - 1):
      for y in range(0, self.config['height']):
        if (x is 0 or x is self.config['width'] - 2 or y is 0 or y is self.config['height'] - 1):
          self.window.addstr(y, x, ".", curses.color_pair(6))

