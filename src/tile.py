# import curses

class Tile:

  def __init__(self, x, y):
    self.type = "empty"
    self.x = x
    self.y = y
    self.revealed = False
    self.visible = False
    self.in_periphery = False

  def char(self):
    chars = {
        "floor": ".", "wall": " ", "empty": " ", "corridor": "#",
        "stairs_down": ">", "stairs_up": "<"
      }
    return chars[self.type]

  def color(self, curses):
    colors = {
        "floor": 4, "wall": 5, "empty": 1, "corridor": 3,
        "stairs_down": 2, "stairs_up": 2
      }
    return curses.color_pair(colors[self.type])

  def set_type(self, new_type):
    self.type = new_type

  def walkable(self):
    walkables = ["floor", "corridor", "stairs_down", "stairs_up"]
    return walkables.count(self.type) > 0

  def draw(self, curses, screen):
    return screen.addstr(self.y, self.x, self.char(), self.color(curses))

  def odd(self):
    return self.x % 2 != 0 and self.y % 2 != 0

  def empty(self):
    return self.type is "empty"

  def get_neighbors(self, tiles):
    tiles_at_distance_two = list(filter(lambda tile: tile.at_distance(2, self), tiles))
    empty_at_distance_two = list(filter(lambda tile: tile.empty(), tiles_at_distance_two))
    return empty_at_distance_two

  def at_distance(self, n, target):
    if (target.x is self.x):
      return (target.y is self.y - n or
              target.y is self.y + n)
    elif (target.y is self.y):
      return (target.x is self.x - n or
              target.x is self.x + n)
    else:
      return False

  def direction_from(self, tile):
    x = 0
    y = 0
    x = -1  if self.x < tile.x else x
    x = 1 if self.x > tile.x else x
    y = -1  if self.y < tile.y else y
    y = 1 if self.y > tile.y else y
    return (x, y)

  def dead_end(self, adjacents):
    empties = list(filter(lambda tile: tile.empty(), adjacents))
    walkables = list(filter(lambda tile: tile.walkable(), adjacents))
    return (len(empties) is (len(adjacents) - 1) and len(walkables) is 1
            and self.type is "corridor")

