from tile import Tile
import random

class Level:

  def __init__(self, config):
    self.tiles = []
    self.width = config['width']
    self.height = config['height']
    self.room_settings = config['rooms']

  def generate(self, config):
    self.create_empty_tiles()
    generator = Generator()
    generator.generate_level(self, config)

  def create_empty_tiles(self):
    for x in range(0,self.width):
      self.tiles.append([])
      for y in range(0,self.height):
        self.tiles[x].append(None)
        tile = Tile(x,y)
        tile.set_type('empty')
        self.tiles[x][y] = tile

  def draw(self, screen):
    for x in range(0,self.width):
      for y in range(0,self.height):
        self.tiles[x][y].draw(screen)


class Generator:

  def __init__(self):
    self.rooms = []

  def generate_level(self, level, config):
    self.level = level
    self.config = config
    self.generate_rooms()
    self.insert_rooms_into_level()

  def generate_rooms(self):
    room_config = self.config['rooms']
    for attempt in range(0, room_config['generation_attempts']):
      room = self.generate_odd_sized_room(room_config)
      if (room.isolated_from_rooms(self.rooms) and room.within_level(self.level)):
        self.rooms.append(room)

  def generate_odd_sized_room(self, room_config):
    x = self.odd_number(0, self.config['width'])
    y = self.odd_number(0, self.config['height'])
    wd = self.odd_number(room_config['min_width'], room_config['max_width'])
    ht = self.odd_number(room_config['min_height'], room_config['max_height'])
    return Room(x, y, wd, ht)

  def odd_number(self, min_, max_):
    number = (random.randint(min_, max_))
    if (number % 2 == 0):
      return number + 1
    else:
      return number

  def insert_rooms_into_level(self):
    level = self.level
    for room in self.rooms:
      for column in range (room.x, room.x + room.width):
        for row in range (room.y, room.y + room.height):
          level.tiles[column][row].set_type('floor')


class Room:

  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def collides_with_room(self, room):
    if (self.x > room.x + room.width or self.y > room.y + room.height):
      return False
    elif (self.x + self.width < room.x or self.y + self.height < room.y):
      return False
    else:
      return True

  def isolated_from_rooms(self, rooms):
      colliding_rooms = list(
          filter(lambda room: self.collides_with_room(room), rooms)
      )
      return (len(colliding_rooms) == 0)

  def within_level(self, level):
    return (self.x + self.width < level.width and
        self.y + self.height < level.height)

