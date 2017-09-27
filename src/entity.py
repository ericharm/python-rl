class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y

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

  def set_state(self, state):
    self.state = state

  def char(self):
    return "@"

  def color(self, curses):
    return curses.color_pair(5)


