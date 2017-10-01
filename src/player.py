class Player:

  def __init__(self, game):
    self.game = game

  def handle_input(self, key):
    hero = self.game.hero
    tiles = self.game.level.tiles
    x = hero.x
    y = hero.y
    if   (key == "KEY_LEFT" and self.game.is_walkable(x - 1, y)):
      tiles[x][y].entities.remove(hero)
      tiles[x-1][y].entities.append(hero)
      hero.x -= 1
    elif (key == "KEY_RIGHT" and self.game.is_walkable(x + 1, y)):
      tiles[x][y].entities.remove(hero)
      tiles[x+1][y].entities.append(hero)
      hero.x += 1
    elif (key == "KEY_UP" and self.game.is_walkable(x, y - 1)):
      tiles[x][y].entities.remove(hero)
      tiles[x][y-1].entities.append(hero)
      hero.y -= 1
    elif (key == "KEY_DOWN" and self.game.is_walkable(x, y + 1)):
      tiles[x][y].entities.remove(hero)
      tiles[x][y+1].entities.append(hero)
      hero.y += 1
    elif (key is ">" and self.game.level.tiles[x][y].type is "stairs_down"):
      self.game.descend_stairs()
    elif (key is "<" and self.game.level.tiles[x][y].type is "stairs_up"):
      self.game.ascend_stairs()
    elif (key is "q"):
      return False

