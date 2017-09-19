class Entity:

  def __init__(self, x, y):
    self.x = x
    self.y = y

class Hero (Entity):

  def __init__(self, x, y):
    Entity.__init__(self, x, y)
    self.state = "moving"

  def set_state(self, state):
    self.state = state
