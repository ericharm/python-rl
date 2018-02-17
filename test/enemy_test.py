import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.entity import *

class EnemyTest(unittest.TestCase):

  def test_in_acting_range(self):
    hero = Hero(0, 0)
    enemy = Enemy(5, 0)
    enemy.acting_range = 4
    self.assertFalse(enemy.in_acting_range(hero))
    enemy.acting_range = 5
    self.assertTrue(enemy.in_acting_range(hero))

