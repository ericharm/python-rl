from entity import Zap

class Player:

  def __init__(self, game):
    self.game = game

  def add_zap_to_level(self, hero, velocity):
    zap = Zap(hero.x, hero.y)
    self.game.level.entities.append(zap)
    hero.decrement_zaps()
    zap.set_velocity(velocity[0], velocity[1])

  def handle_input(self, key):
    hero = self.game.hero
    tiles = self.game.level.tiles
    x = hero.x
    y = hero.y
    if (hero.state is "moving"):
        if (key == "KEY_LEFT" and self.game.is_walkable(x - 1, y)):
          hero.move(-1, 0)
        elif (key == "KEY_RIGHT" and self.game.is_walkable(x + 1, y)):
          hero.move(1, 0)
        elif (key == "KEY_UP" and self.game.is_walkable(x, y - 1)):
          hero.move(0, -1)
        elif (key == "KEY_DOWN" and self.game.is_walkable(x, y + 1)):
          hero.move(0, 1)
        elif (key is ">" and self.game.level.tiles[x][y].type is "stairs_down"):
          self.game.descend_stairs()
        elif (key is "<" and self.game.level.tiles[x][y].type is "stairs_up"):
          self.game.ascend_stairs()
        elif (key is " "):
            hero.set_state("aiming")
        elif (key is "q"):
          return False
    elif (hero.state is "aiming"):
        hero.set_state("moving")
        if (key == "KEY_LEFT" and self.game.is_walkable(x - 1, y)):
          self.add_zap_to_level(hero, (-1, 0))
        elif (key == "KEY_RIGHT" and self.game.is_walkable(x + 1, y)):
          self.add_zap_to_level(hero, (1, 0))
        elif (key == "KEY_UP" and self.game.is_walkable(x, y - 1)):
          self.add_zap_to_level(hero, (0, -1))
        elif (key == "KEY_DOWN" and self.game.is_walkable(x, y + 1)):
          self.add_zap_to_level(hero, (0, 1))
        else:
          return True

