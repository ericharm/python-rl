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
    generator = Generator(self, config)
    generator.generate_rooms()

  def create_empty_tiles(self):
    for x in range(0,self.width):
      self.tiles.append([])
      for y in range(0,self.height):
        self.tiles[x].append(None)
        tile = Tile(x,y)
        self.tiles[x][y] = tile

  def draw(self, screen):
    for x in range(0,self.width):
      for y in range(0,self.height):
        self.tiles[x][y].draw(screen)


class Generator:

  def __init__(self, level, config):
    self.level = level
    self.config = config
    self.rooms = []

  def generate_rooms(self):
    rooms = self.config['rooms']
    for attempt in range(0, rooms['generation_attempts']):
      odd_x = 1 + (random.randint(0, self.config['width']) * 2) / 2 + 1
      odd_y = 1 + (random.randint(0, self.config['height']) * 2) / 2 + 1

      rooms = self.config['rooms']
      odd_width = (random.randint(rooms['min_width'],
                                  rooms['max_width']) * 2) / 2 + 1
      odd_height = (random.randint(rooms['min_height'],
                                   rooms['max_height']) * 2) / 2 + 1

      room = Room(odd_x, odd_y, odd_width, odd_height)
      self.add_room_if_isolated(room)
    self.insert_rooms_into_level()

  def add_room_if_isolated(self, new_room):
      colliding_rooms = list(
          filter(lambda room: room.collides_with(new_room), self.rooms)
      )
      if (len(colliding_rooms) == 0):
        self.rooms.append(new_room)

  def insert_rooms_into_level(self):
    level = self.level
    for room in self.rooms:
      for column in range(room.x, room.x + room.width):
        for row in range(room.y, room.y + room.height):
          if (column < level.width and row < level.height):
            level.tiles[column][row].set_type("floor")


class Room:

  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

  def collides_with(self, room):
    if (self.x > room.x + room.width or self.y > room.y + room.height):
      return False
    elif (self.x + self.width < room.x or self.y + self.height < room.y):
      return False
    else:
      return True

