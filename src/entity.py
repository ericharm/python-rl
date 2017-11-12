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

  def move(self, x, y):
    # tiles[self.x][self.y].entities.remove(self)
    self.x += x
    self.y += y
    # tiles[self.x][self.y].entities.append(self)

  def update(self, level):
    return True

class Hero (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.state = "moving"
    self.zaps = 2
    self.inventory = [{"name": "Health", "quantity": 3},
                      {"name": "Rocks",  "quantity": 8},
                      {"name": "Zapgun Charges", "quantity": 2}]

  def set_state(self, state):
    self.state = state

  def char(self):
    return "@"

  def color(self, curses):
    return curses.color_pair(5)

  def decrement_zaps(self):
    zaps = list(filter(lambda item: item['name'] == 'Zapgun Charges', self.inventory))
    if (len(zaps) > 0):
      zaps[0]['quantity'] -= 1


class Enemy (Entity):

  def char(self):
    return "a"

  def color(self, curses):
    return curses.color_pair(7)


class Zap (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.velocity = { "x": x, "y": y }

  def char(self):
    if (self.velocity["x"] is 0):
      return "|"
    elif (self.velocity["y"] is 0):
      return "-"
    else:
      return "?"

  def color(self, curses):
    return curses.color_pair(6)

  def set_velocity(self, x, y):
    self.velocity = { "x": x, "y": y }

  def update(self, level):
    destination_x = self.x + self.velocity["x"]
    destination_y = self.y + self.velocity["y"]
    if (level.tiles[destination_x][destination_y].walkable()):
      self.move(self.velocity["x"], self.velocity["y"])
    else:
      level.entities.remove(self)



