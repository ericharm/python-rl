from src.util import *
from src.pather import Pather
from functools import reduce

class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.inventory = []
    self.categories = ['entity']

  def char(self):
    return ' '

  def color(self): # pragma: no cover
    return Color.use('black')

  def move(self, x, y, level):
    dest_vec = Vector(self.x + x, self.y + y)
    destination = level.tiles[dest_vec.x][dest_vec.y]
    if (destination.x < (level.width - 1) and destination.y < (level.height - 1)
    and destination.walkable()):
      self.x += x
      self.y += y
      if len(self.colliding_entities(level.entities)) != 0:
        self.x -= x
        self.y -= y

  def draw(self, screen): # pragma: no cover
    return screen.addstr(self.y, self.x, self.char(), self.color())

  def update(self, level):
    del level
    return True

  def distance_from_entity(self, entity):
    return Vector(entity.x - self.x, entity.y - self.y).length()

  def colliding_entities(self, entities):
    return list(filter(lambda entity: self.is_colliding_with(entity), entities))

  def is_colliding_with(self, entity):
    return entity.x == self.x and entity.y == self.y and entity != self

  def pluck(self, level):
    level.entities.remove(self)


class Hero (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.is_hero = True
    self.state = 'moving'
    #  self.zaps = 12
    self.categories.extend(['hero', 'shootable'])
    self.inventory = [{'name': 'Health', 'quantity': 3},
                      {'name': 'Rocks',  'quantity': 8},
                      {'name': 'Zapgun Charges', 'quantity': 12}]

  def set_state(self, state):
    self.state = state
    return self

  def char(self):
    return '@'

  def color(self): # pragma: no cover
    return Color.use('magenta')

  def set_aiming(self):
    if self.get_zaps()['quantity'] > 0:
      self.set_state('aiming')

  def decrement_zaps(self):
    self.get_zaps()['quantity'] -= 1

  def get_zaps(self):
    return reduce(lambda a, b: a if a['name'] == 'Zapgun Charges' else b, self.inventory)


class Enemy (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.acting_range = 10
    self.categories.extend(['enemy', 'shootable'])

  def char(self):
    return 'a'

  def color(self): # pragma: no cover
    return Color.use('yellow')

  def in_acting_range(self, hero):
    return True if self.distance_from_entity(hero) <= self.acting_range else False

  def move(self, hero, level):
    tiles = level.flattened_tiles
    my_tile = reduce(lambda a, b: a if a.x is self.x and a.y is self.y else b, tiles)
    hero_tile = reduce(lambda a, b: a if a.x is hero.x and a.y is hero.y else b, tiles)
    pather = Pather(my_tile, level)
    path = pather.get_path(hero_tile)
    if path != None and len(path) > 0:
      self.x = path[0][0]
      self.y = path[0][1]

  def update(self, level):
    hero = reduce((lambda a, b: a if 'hero' in a.categories else b), level.entities)
    if self.in_acting_range(hero):
      self.move(hero, level)


class Zap (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.velocity = Vector(x, y)
    self.categories.extend(['zap'])

  def char(self):
    return '|' if self.velocity.x == 0 else '-'

  def color(self): # pragma: no cover
    return Color.use('white')

  def set_velocity(self, x, y):
    self.velocity = Vector(x, y)
    return self

  def update(self, level):
    destination = Vector(self.x + self.velocity.x, self.y + self.velocity.y)
    if destination.in_level(level) and level.tiles[destination.x][destination.y].walkable():
      self.move(self.velocity.x, self.velocity.y, level)
    else:
      level.entities.remove(self)

