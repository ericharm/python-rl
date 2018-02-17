import math
import random

class Vector:

  def __init__(self, x, y):
    self.x = x
    self.y = y

  def length(self):
    return math.sqrt(self.x ** 2 + self.y ** 2)

  def to_binary(self):
    coords = map(lambda value: 0 if value is 0 else value / abs(value), [self.x, self.y])
    self.x = coords[0]
    self.y = coords[1]
    return self
    

class Chance:

  @staticmethod
  def flip_coin():
    return random.choice([True, False])
