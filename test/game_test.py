import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.game import Game
from src.player import Player

class MockKeyboard:
  def __init__(self, key):
    self.key = key

  def getkey(self):
    return self.key

class GameTest(unittest.TestCase):

  def setUp(self):
    self.config = {
      'game': {
        'levels': 5 
      },
      'level': {
        'width': 10,
        'height': 10,
        'rooms': {
          'min_width': 3, 'min_height': 3,
          'max_width': 3, 'max_height': 3,
          'generation_attempts': 10
        },
        'corridors': { 'dead_end_removals': 0 }
      }
    }

  def test_staircases_generate_levels(self):
    self.config['game']['levels'] = 5
    game = Game(self.config)
    game.update()
    for level in range(0, self.config['game']['levels']):
      game.descend_stairs()
    self.assertEqual(5, game.current_level)
    game.ascend_stairs()
    self.assertEqual(4, game.current_level)

  def test_handle_input(self):
    self.config['game']['levels'] = 5
    game = Game(self.config)
    game.hero.x = 5
    game.hero.y = 5
    game.level.tiles[4][5].set_type('floor')
    game.player = Player(game)
    game.handle_input(MockKeyboard("KEY_LEFT"))
    self.assertEqual(4, game.hero.x)

