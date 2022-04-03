from src.util import Color
from src.game import Game

class Title:

  def __init__(self, config, state_stack):
    self.config = config
    self.state_stack = state_stack
    self.options = ['start', 'exit']
    self.current_option = 0

  def draw(self, windows): # pragma: no cover
    body = windows['body']
    body.clear()
    line = 10
    body.addstr(line - 2, 20, 'SPACE JAIL', Color.use('red'))
    body.addstr(line + self.current_option, 20, '#', Color.use('blue'))
    for option in self.options:
      body.addstr(line, 22, option.capitalize(), Color.use('white'))
      line += 1

  def handle_input(self, key):
    if key == 'q':
      return False
    elif key == 'KEY_DOWN' and self.current_option < len(self.options) - 1:
      self.current_option += 1
    elif key == 'KEY_UP' and self.current_option > 0:
      self.current_option -= 1
    elif key == '\n':
      return self.set_state()
    return True

  def update(self):
    return True

  def set_state(self):
    if (self.options[self.current_option] == 'start'):
      self.state_stack.remove(self)
      self.state_stack.append(Game(self.config,self.state_stack))
    if (self.options[self.current_option] == 'exit'):
      return False

