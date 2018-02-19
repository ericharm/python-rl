from tile import Tile
from entity import Enemy
from collision_controller import CollisionController
import random

class Level:

  def __init__(self, config):
    self.config = config
    self.tiles = []
    self.entities = []
    self.plucked = []
    self.rooms = []
    self.collision_controller = CollisionController(self)
    self.width = config['width']
    self.height = config['height']

  def draw(self, screen): # pragma: no cover
    for x in range(0,self.width):
      for y in range(0,self.height):
        self.tiles[x][y].draw(screen)
    for entity in range(0, len(self.entities)):
      self.entities[entity].draw(screen)

  def update(self):
    for entity in reversed(self.entities):
      entity.update(self)
    self.collision_controller.handle_collisions(self.entities)

  def generate(self):
    self.create_empty_tiles()
    self.generate_rooms()
    self.generate_corridors()
    self.insert_rooms()
    for times in range(0, 20):
      self.remove_dead_ends()
    self.insert_enemies()
    return self

  def with_stairs_up(self, hero):
    self.tiles[hero.x][hero.y].set_type("stairs_up")
    return self

  def with_stairs_down(self):
    tile = self.get_random_floor_tile()
    tile.set_type('stairs_down')
    return self

  # private
  def insert_enemies(self):
    enemies = 0
    while enemies < 3:
      tile = self.get_random_walkable_unoccupied_tile()
      self.entities.append(Enemy(tile.x, tile.y))
      enemies = enemies + 1

  def generate_rooms(self):
    room_config = self.config['rooms']
    for attempt in range(0, room_config['generation_attempts']):
      room = self.generate_odd_sized_room(room_config)
      if (room.isolated_from_rooms(self.rooms) and room.within_level(self)):
        self.rooms.append(room)

  def generate_odd_sized_room(self, room_config):
    x = self.odd_number(0, self.config['width'])
    y = self.odd_number(0, self.config['height'])
    wd = self.odd_number(room_config['min_width'], room_config['max_width'])
    ht = self.odd_number(room_config['min_height'], room_config['max_height'])
    return Room(x, y, wd, ht)

  def generate_corridors(self):
    while len(self.get_odd_empty_tiles()) > 0:
      tiles = self.get_odd_empty_tiles()
      tree = [tiles[0]] # could start at a random instead
      self.generate_corridor(tiles, tree, tiles[0])

  def generate_corridor(self, tiles, tree, source_tile):
    # build a corridor using recursive maze generation algorithm
    current_tile = source_tile
    while len(tree) > 0:
      neighbors = current_tile.get_neighbors(tiles)
      if len(neighbors) > 0:
        neighbor = neighbors[random.randint(0, len(neighbors)) - 1]
        self.connect_neighbors_as_corridor(current_tile, neighbor)
        current_tile = neighbor
        tree.append(current_tile)
      else:
        current_tile = tree.pop()

  def connect_neighbors_as_corridor(self, source_tile, target_tile):
    source_tile.set_type("corridor")
    target_x = target_tile.x
    target_y = target_tile.y
    self.tiles[target_x][target_y].set_type("corridor")
    direction = target_tile.direction_from(source_tile)
    between_x = direction[0] + source_tile.x
    between_y = direction[1] + source_tile.y
    self.tiles[between_x][between_y].set_type("corridor")

  def odd_number(self, min_, max_):
    number = (random.randint(min_, max_))
    if (number % 2 is 0):
      return number + 1
    else:
      return number

  def create_empty_tiles(self):
    for x in range(0, self.width):
      self.tiles.append([])
      for y in range(0, self.height):
        self.tiles[x].append(None)
        tile = Tile(x,y)
        self.tiles[x][y] = tile
    return self

  def insert_rooms(self):
    for room in self.rooms:
      for column in range (room.x, room.x + room.width):
        for row in range (room.y, room.y + room.height):
          self.tiles[column][row].set_type('floor')

  def get_random_floor_tile(self):
    random_tile = self.get_random_tile()
    while random_tile.type != 'floor':
      random_tile = self.get_random_tile()
    return random_tile

  def get_random_walkable_unoccupied_tile(self):
    random_tile = self.get_random_tile()
    while not (random_tile.walkable() and not self.tile_occupied(random_tile)):
      random_tile = self.get_random_tile()
    return random_tile

  def tile_occupied(self, tile):
    occupied_tiles = list(
        filter(lambda entity: self.tiles[entity.x][entity.y], self.entities)
    )
    return (tile in occupied_tiles)

  def get_random_tile(self):
    x = random.randint(0, self.width - 1)
    y = random.randint(0, self.height - 1)
    return self.tiles[x][y]

  def get_odd_empty_tiles(self):
    odd_empty_tiles = []
    for column in range(0, self.width):
      for row in range(0, self.height):
        if self.tiles[column][row].empty() and self.tiles[column][row].odd():
          odd_empty_tiles.append(self.tiles[column][row])
    return odd_empty_tiles

  def get_adjacent_tiles(self, x, y):
    adjacents = []
    if (x > 1):
      adjacents.append(self.tiles[x-1][y])
    if (x < self.width - 1):
      adjacents.append(self.tiles[x+1][y])
    if (y > 1):
      adjacents.append(self.tiles[x][y-1])
    if (y < self.height - 1):
      adjacents.append(self.tiles[x][y+1])
    return adjacents

  def remove_dead_ends(self):
    for column in range(0, self.width):
      for row in range(0, self.height):
        tile = self.tiles[column][row]
        adjacents = self.get_adjacent_tiles(column, row)
        if (tile.type is "corridor" and tile.dead_end(adjacents)):
          tile.set_type("empty");


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
      return (len(colliding_rooms) is 0)

  def within_level(self, level):
    return (self.x + self.width < level.width and
        self.y + self.height < level.height)


