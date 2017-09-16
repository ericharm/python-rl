class Tile:

  def __init__(self, x, y):
    self.type = "empty"
    self.location = {"x": x, "y": y}
    self.revealed = False
    self.visible = False
    self.in_periphery = False

  def char(self):
    if self.type is "floor":
      return "."
    elif self.type is "wall":
      return "#"
    elif self.type is "empty":
      return " "
    elif self.type is "corridor":
      return "#"
    elif self.type is "stairs_down":
      return ">"

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

  def walkable(self):
    # change this to hold an array of walkable types and search that array
    return self.type is "floor" or self.type is "corridor" or self.type is "stairs_down"

  def draw(self, screen):
     screen.addstr(self.location['y'], self.location['x'], self.char())

  def odd(self):
    return self.location['x'] % 2 != 0 and self.location['y'] % 2 != 0

  def empty(self):
    return self.type is "empty"

  def get_neighbors(self, tiles):
    tiles_at_distance_two = list(filter(lambda tile: tile.at_distance(2, self), tiles))
    empty_at_distance_two = list(filter(lambda tile: tile.empty(), tiles_at_distance_two))
    return empty_at_distance_two

  def at_distance(self, n, target):
    if (target.location['x'] is self.location['x']):
      return (target.location['y'] is self.location['y'] - n or
              target.location['y'] is self.location['y'] + n)
    elif (target.location['y'] is self.location['y']):
      return (target.location['x'] is self.location['x'] - n or
              target.location['x'] is self.location['x'] + n)
    else:
      return False

  def direction_from(self, tile):
    x = 0
    y = 0
    x = -1  if self.location['x'] < tile.location['x'] else x
    x = 1 if self.location['x'] > tile.location['x'] else x
    y = -1  if self.location['y'] < tile.location['y'] else y
    y = 1 if self.location['y'] > tile.location['y'] else y
    return (x, y)

