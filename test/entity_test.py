import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.entity import *
from src.level import Level

class EntityTest(unittest.TestCase):

  def test_hero_initial_state_is_moving(self):
    hero = Hero(1, 2)
    self.assertEqual("moving", hero.state)

  def test_distance_from(self):
    hero = Hero(2, 5)
    enemy = Enemy(5,9)
    self.assertEqual(5, hero.distance_from_entity(enemy))

