import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.entity import *

class EntityTest(unittest.TestCase):

  def test_hero_initial_state_is_moving(self):
    hero = Hero(1, 2)
    self.assertEqual("moving", hero.state)

