class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y

class Hero (Entity):

  def set_state(self, state):
    self.state = state
