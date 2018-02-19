import os
import sys
import unittest

sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.application import Application
from src.game import Game
from src.game_input_controller import GameInputController
from src.entity import Zap

class GameTest(unittest.TestCase):

  def setUp(self):
    self.config = {
      'game': {
        'levels': 3 
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
      },
      'windows': {
        'footer': {
          'width': 10,
          'height': 5
        }
      }
    }

  def test_application(self):
    app = Application(self.config)
    self.assertEqual([], app.states)

  def test_staircases_generate_levels(self):
    self.config['game']['levels'] = 3
    game = Game(self.config, [])
    for level in range(0, self.config['game']['levels']):
      game.descend_stairs()
    self.assertEqual(3, game.current_level)
    game.ascend_stairs()
    self.assertEqual(2, game.current_level)

  def test_handle_input(self):
    self.config['game']['levels'] = 3
    game = Game(self.config, [])
    game.hero.x = 5
    game.hero.y = 5
    game.level.tiles[4][5].set_type('floor')
    game.player = GameInputController(game)
    game.handle_input("KEY_LEFT")
    self.assertEqual(4, game.hero.x)

  def test_handle_input_exception(self):
    self.config['game']['levels'] = 3
    game = Game(self.config, [])
    game.hero.x = 5
    game.hero.y = 5
    game.level.tiles[4][5].set_type('floor')
    game.player = GameInputController(game)
    self.assertEqual(None, game.handle_input(None))

  def test_update_game(self):
    self.config['game']['levels'] = 3
    game = Game(self.config, [])
    game.level.tiles[0][0].set_type('floor')
    game.level.tiles[1][0].set_type('floor')
    zap = Zap(1, 0).set_velocity(-1, 0)
    game.level.entities = [zap]
    game.update()
    self.assertEqual((0, 0), (zap.x, zap.y))
    
