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
    self.insert_rooms(generator.rooms)
    generator.generate_corridors()

  def create_empty_tiles(self):
    for x in range(0,self.width):
      self.tiles.append([])
      for y in range(0,self.height):
        self.tiles[x].append(None)
        tile = Tile(x,y)
        tile.set_type('empty')
        self.tiles[x][y] = tile

  def insert_rooms(self, rooms):
    for room in rooms:
      self.insert_walls(room)
      for column in range (room.x, room.x + room.width):
        for row in range (room.y, room.y + room.height):
          self.tiles[column][row].set_type('floor')

  def insert_walls(self, room): # needs test
    x = room.x - 1
    y = room.y - 1
    width = room.width + 2
    height = room.height + 2
    for column in range (x, x + width):
      for row in range (y, y + height):
        self.tiles[column][row].set_type('wall')

  def get_odd_empty_tiles(self): # needs test
    odd_empty_tiles = []
    for column in range(0, self.width):
      for row in range(0, self.height):
        if self.tiles[column][row].empty() and self.tiles[column][row].odd():
          odd_empty_tiles.append(self.tiles[column][row])
    return odd_empty_tiles

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

  def generate_corridors(self): # might not need test
    tiles = self.level.get_odd_empty_tiles() # get back to this
    current_tile = tiles[0]
    tree = [current_tile]

    neighbors = current_tile.get_neighbors(tiles)
    while len(neighbors) > 0:
      neighbor = neighbors[random.randint(0, len(neighbors)) - 1]
      current_tile.set_type("corridor")

      target_x = neighbor.location['x']
      target_y = neighbor.location['y']
      self.level.tiles[target_x][target_y].set_type("corridor")

      direction = neighbor.direction_from(current_tile)
      between_x = direction[0] + target_x
      between_y = direction[1] + target_y
      self.level.tiles[between_x][between_y].set_type("corridor")

      current_tile = neighbor
      tree.append(current_tile)
      neighbors = current_tile.get_neighbors(tiles)
    # once neighbors equals zero,
    # climb down the tree


  def odd_number(self, min_, max_):
    number = (random.randint(min_, max_))
    if (number % 2 == 0):
      return number + 1
    else:
      return number


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

