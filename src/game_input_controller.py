from entity import Zap
from util import Vector

class GameInputController:

  def __init__(self, game):
    self.game = game
    self.hero = game.hero
    self.movement_keys = {
        "KEY_LEFT": (-1, 0),
        "KEY_RIGHT": (1, 0),
        "KEY_UP": (0, -1),
        "KEY_DOWN": (0, 1),
      }

  def handle_input(self, key):
    if (self.hero.state is "moving"):
      return self.handle_movement_action(key)
    elif (self.hero.state is "aiming"):
      return self.handle_aiming_action(key)

  def handle_movement_action(self, key):
    x = self.hero.x
    y = self.hero.y
    tiles = self.game.level.tiles
    if (key in self.movement_keys.keys()):
      vector = self.movement_keys[key]
      self.hero.move(vector[0], vector[1], self.game.level);
    elif (key is ">" and tiles[x][y].type is "stairs_down"):
      self.game.descend_stairs()
    elif (key is "<" and tiles[x][y].type is "stairs_up"):
      self.game.ascend_stairs()
    elif (key is " "):
        self.hero.set_aiming()
    elif (key is "q"):
      return False

  def handle_aiming_action(self, key):
    self.hero.set_state("moving")
    if (key in self.movement_keys.keys()):
      vector = Vector(self.movement_keys[key][0], self.movement_keys[key][1])
      zap = Zap(self.hero.x, self.hero.y)
      self.add_zap_at_vector(zap, vector)
    else:
      return True

  def add_zap_at_vector(self, zap, vector):
    destination_x = zap.x + vector.x
    destination_y = zap.y + vector.y
    if (self.game.level.tiles[destination_x][destination_y].walkable()):
      self.game.level.entities.append(zap)
      self.hero.decrement_zaps()
      zap.set_velocity(vector.x, vector.y)

