class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.inventory = []
    self.draw_priority = 1
    self.update_priority = 1
    self.shootable = True

  def char(self):
    return " "

  def color(self, curses):
    return curses.color_pair(1)

  def move(self, x, y):
    self.x += x
    self.y += y

  def draw(self, curses, screen):
    return screen.addstr(self.y, self.x, self.char(), self.color(curses))

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
    self.shootable = False

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
      for entity in reversed(level.entities):
        if entity.x is self.x and entity.y is self.y and entity.shootable:
          level.entities.remove(entity)
          level.entities.remove(self)
    else:
      level.entities.remove(self)


