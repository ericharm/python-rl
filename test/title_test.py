import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.title import Title
from src.game import Game
from test.fixtures import Fixtures

class TitleScreenTest(unittest.TestCase):

  def setUp(self):
    config = Fixtures.game_config
    self.title = Title(config, [])
    self.title.state_stack.append(self.title)

  def test_arrow_keys_change_options(self):
    title = self.title
    self.assertEqual('start', title.options[title.current_option])
    title.handle_input('KEY_DOWN')
    self.assertEqual('exit', title.options[title.current_option])
    title.handle_input('KEY_UP')
    self.assertEqual('start', title.options[title.current_option])

  def test_q_button_quits(self):
    self.assertFalse(self.title.handle_input('q'))

  def test_update_simply_returns_true(self):
    self.assertTrue(self.title.update())

  def test_enter_key_on_exit_returns_false(self):
    self.title.handle_input('KEY_DOWN')
    self.title.handle_input('\n')
    self.assertFalse(self.title.set_state())

  def test_enter_key_on_start_moves_new_game_onto_stack(self):
    self.title.handle_input('\n')
    self.assertIsInstance(self.title.state_stack[0], Game)

