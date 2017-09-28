class Player:

  def __init__(self, game):
    self.game = game

  def handle_input(self, key):
    hero = self.game.hero
    x = hero.x
    y = hero.y
    if   (key == "KEY_LEFT" and self.is_walkable(x - 1, y)):
      hero.x -= 1
    elif (key == "KEY_RIGHT" and self.is_walkable(x + 1, y)):
      hero.x += 1
    elif (key == "KEY_UP" and self.is_walkable(x, y - 1)):
      hero.y -= 1
    elif (key == "KEY_DOWN" and self.is_walkable(x, y + 1)):
      hero.y += 1
    elif (key is ">" and self.game.level.tiles[x][y].type is "stairs_down"):
      self.descend_stairs()
    elif (key is "<" and self.game.level.tiles[x][y].type is "stairs_up"):
      self.ascend_stairs()
    elif (key is "q"):
      return False

  def descend_stairs(self): #
    self.current_level += 1
    if len(self.levels) <= self.current_level:
      level = self.generate_next_level()
      self.levels.append(level)
    self.game.level = self.game.levels[self.current_level]

  def ascend_stairs(self): #
    self.game.current_level -= 1
    self.game.level = self.game.levels[self.current_level]

  def is_walkable(self, x, y): #
    if y >= self.game.level.height or x >= self.game.level.width:
      return False
    return self.game.level.tiles[x][y].walkable()

