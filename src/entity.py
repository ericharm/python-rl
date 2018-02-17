from util import *

class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.inventory = []
    self.draw_priority = 1
    self.update_priority = 1
    self.shootable = True
    self.is_hero = False

  def char(self):
    return ' '

  def color(self, curses):
    return curses.color_pair(1)

  def move(self, x, y, level):
    destination_x = self.x + x
    destination_y = self.y + y
    if (level.tiles[destination_x][destination_y].walkable()):
      self.x += x
      self.y += y

  def draw(self, curses, screen):
    return screen.addstr(self.y, self.x, self.char(), self.color(curses))

  def update(self, level):
    return True

  def distance_from_entity(self, entity):
    return Vector(entity.x - self.x, entity.y - self.y).length()


class Hero (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.is_hero = True
    self.state = 'moving'
    self.zaps = 2
    self.inventory = [{'name': 'Health', 'quantity': 3},
                      {'name': 'Rocks',  'quantity': 8},
                      {'name': 'Zapgun Charges', 'quantity': 2}]

  def set_state(self, state):
    self.state = state

  def char(self):
    return '@'

  def color(self, curses):
    return curses.color_pair(5)

  def decrement_zaps(self):
    zaps = list(filter(lambda item: item['name'] == 'Zapgun Charges', self.inventory))
    if (len(zaps) > 0):
      zaps[0]['quantity'] -= 1


class Enemy (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.acting_range = 10

  def char(self):
    return 'a'

  def color(self, curses):
    return curses.color_pair(7)

  def in_acting_range(self, hero):
    return True if self.distance_from_entity(hero) <= self.acting_range else False

  def move(self, hero, level):
    line_to_hero = Vector(hero.x - self.x, hero.y - self.y)
    movement = (Vector(line_to_hero.x, 0) if abs(line_to_hero.x) > abs(line_to_hero.y)
    else Vector(0, line_to_hero.y)).to_binary()
    Entity.move(self, movement.x, movement.y, level)

  def update(self, level):
    hero = reduce((lambda a, b: a if a.is_hero else b), level.entities)
    if self.in_acting_range(hero) and Chance.flip_coin():
      self.move(hero, level)


class Zap (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.velocity = { 'x': x, 'y': y }
    self.shootable = False

  def char(self):
    if (self.velocity['x'] is 0):
      return '|'
    elif (self.velocity['y'] is 0):
      return '-'
    else:
      return '?'

  def color(self, curses):
    return curses.color_pair(6)

  def set_velocity(self, x, y):
    self.velocity = { 'x': x, 'y': y }

  def update(self, level):
    destination_x = self.x + self.velocity['x']
    destination_y = self.y + self.velocity['y']
    if (level.tiles[destination_x][destination_y].walkable()):
      self.move(self.velocity['x'], self.velocity['y'], level)
      for entity in reversed(level.entities):
        if entity.x is self.x and entity.y is self.y and entity.shootable:
          level.entities.remove(entity)
          level.entities.remove(self)
    else:
      level.entities.remove(self)


