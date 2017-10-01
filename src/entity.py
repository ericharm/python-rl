class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.inventory = []

  def char(self):
    return " "

  def color(self, curses):
    return curses.color_pair(1)

  def draw(self, curses, screen):
    return screen.addstr(self.y, self.x, self.char(), self.color(curses))


class Hero (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.state = "moving"
    self.inventory = [{"name": "Health", "quantity": 3},
                      {"name": "Rocks",  "quantity": 8},
                      {"name": "Zapgun Charges", "quantity": 2}]

  def set_state(self, state):
    self.state = state

  def char(self):
    return "@"

  def color(self, curses):
    return curses.color_pair(5)


class Enemy (Entity):

  def char(self):
    return "a"

  def color(self, curses):
    curses.color_pair(7)
