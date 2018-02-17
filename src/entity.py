from util import *
import curses

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

  def color(self): # pragma: no cover
    return Color.use('black')

  def move(self, x, y, level):
    destination = Vector(self.x + x, self.y + y)
    if (destination.x < level.width and destination.y < level.height
    and level.tiles[destination.x][destination.y].walkable()):
      self.x += x
      self.y += y

  def draw(self, screen): # pragma: no cover
    return screen.addstr(self.y, self.x, self.char(), self.color())

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
    return self

  def char(self):
    return '@'

  def color(self): # pragma: no cover
    return Color.use('magenta')

  def decrement_zaps(self):
    zaps = reduce(lambda a, b: a if a['name'] is 'Zapgun Charges' else b, self.inventory)
    zaps['quantity'] -= 1


class Enemy (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.acting_range = 10

  def char(self):
    return 'a'

  def color(self): # pragma: no cover
    return Color.use('yellow')

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
    self.velocity = Vector(x, y)
    self.shootable = False

  def char(self):
    return '|' if self.velocity.x is 0 else '-'

  def color(self): # pragma: no cover
    return Color.use('white')

  def set_velocity(self, x, y):
    self.velocity = Vector(x, y)

  def update(self, level):
    destination = Vector(self.x + self.velocity.x, self.y + self.velocity.y)
    if (level.tiles[destination.x][destination.y].walkable()):
      self.move(self.velocity.x, self.velocity.y, level)
      self.handle_entity_collisions(level)
    else:
      level.entities.remove(self)

  def handle_entity_collisions(self, level):
    for entity in reversed(level.entities):
      if entity.x is self.x and entity.y is self.y and entity.shootable:
        level.entities.remove(entity)
        level.entities.remove(self)
