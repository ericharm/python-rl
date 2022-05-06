import os
import sys
import unittest
from functools import reduce

sys.path.insert(0, os.path.abspath(__file__ + "/../.."))

from src.game import Game
from src.entity import Zap
from src.game_input_controller import GameInputController
from test.fixtures import Fixtures


class GameInputControllerTest(unittest.TestCase):
    def setUp(self):
        self.config = Fixtures.game_config
        game = Game(self.config, [])
        self.input_controller = GameInputController(game)
        game.level.tiles[0][0].set_type("floor")
        game.level.tiles[0][1].set_type("floor")
        game.hero.x = 0
        game.hero.y = 0

    def remove_enemies(self, game):
        enemies = list(
            filter(lambda entity: "enemy" in entity.categories, game.level.entities)
        )
        for enemy in enemies:
            game.level.entities.remove(enemy)

    def test_space_key_sets_hero_state_to_aiming(self):
        self.input_controller.handle_input(" ")
        self.assertEqual("aiming", self.input_controller.hero.state)

    def test_arrows_while_aiming_fire_zaps(self):
        game = self.input_controller.game
        self.remove_enemies(game)
        self.input_controller.handle_input(" ")
        self.input_controller.handle_input("KEY_DOWN")
        self.assertEqual("moving", self.input_controller.hero.state)
        zap = reduce(
            lambda a, b: a if a.x == 0 and a.y == 1 else b, game.level.entities
        )
        self.assertIsInstance(zap, Zap)
        self.assertEqual(2, len(game.level.entities))

    def test_non_arrows_while_aiming_just_sets_state_back_to_moving(self):
        game = self.input_controller.game
        self.remove_enemies(game)
        self.input_controller.handle_input(" ")
        self.input_controller.handle_input("p")
        self.assertEqual("moving", self.input_controller.hero.state)
        self.assertEqual(1, len(game.level.entities))

    def test_q_key_quits_game(self):
        self.assertFalse(self.input_controller.handle_input("q"))

    def test_angle_braces_climb_stairs(self):
        game = self.input_controller.game
        self.remove_enemies(game)
        game.level.tiles[0][0].set_type("stairs_down")
        self.input_controller.handle_input(">")
        self.assertEqual(1, game.current_level)
        self.input_controller.handle_input("<")
        self.assertEqual(0, game.current_level)
