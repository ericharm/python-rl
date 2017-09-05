class Tile:

  def __init__(self, x, y):
    self.type = "empty"
    self.location = {"x": x, "y": y}
    self.revealed = False
    self.visible = False
    self.in_periphery = False

  def char(self):
    if self.type == "floor":
      return "."
    elif self.type == "wall":
      return "#"
    elif self.type == "empty":
      return " "
    elif self.type == "sempty":
      return "x"
    elif self.type == "corridor":
      return "="

  def color(self):
    if self.visible:
      return "BRIGHT_WHITE"
    elif self.in_periphery:
      return "WHITE"
    elif self.revealed:
      return "GRAY"
    else:
      return "BLACK"

  def set_type(self, new_type):
    self.type = new_type

  def draw(self, screen):
     screen.addstr(self.location['y'], self.location['x'], self.char())

  def odd(self): # needs test
    return self.location['x'] % 2 != 0 and self.location['y'] % 2 != 0

  def empty(self): # needs test
    return self.type == "empty"

  def get_neighbors(self, tiles):
    tiles_at_distance_two = list(filter(lambda tile: tile.at_distance(2, self), tiles))
    empty_at_distance_two = list(filter(lambda tile: tile.empty(), tiles_at_distance_two))
    return empty_at_distance_two

  # combine at_distance and direction_from
  # we can get the exact x and y difference and infer
  # straight lines and directions later
  def at_distance(self, n, target): # needs test
    is_n_north = (target.location['x'] is self.location['x'] and
                   target.location['y'] is self.location['y'] - n)
    is_n_south = (target.location['x'] is self.location['x'] and
                   target.location['y'] is self.location['y'] + n)
    is_n_west = (target.location['x'] is self.location['x'] - n and
                   target.location['y'] is self.location['y'])
    is_n_east = (target.location['x'] is self.location['x'] + n and
                   target.location['y'] is self.location['y'])
    return (is_n_north or is_n_south or is_n_west or is_n_east)

  def direction_from(self, tile): # needs test
    x = 0
    y = 0
    if self.location['x'] < tile.location['x']:
      x = 1
    if self.location['x'] > tile.location['x']:
      x = -1
    if self.location['y'] < tile.location['y']:
      y = 1
    if self.location['y'] > tile.location['y']:
      y = -1
    return (x, y)

