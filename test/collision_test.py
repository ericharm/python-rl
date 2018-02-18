import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.collision_controller import *
from src.level import Level
from src.entity import *

class CollisionTest(unittest.TestCase):

  def setUp(self):
    self.level = Level({'width' : 10, 'height': 10})
    self.collision_controller = CollisionController(self.level)

  def test_colliding_pairs_control_categories(self):
    entity_a = Entity(0, 0)
    entity_b = Entity(0, 0)
    entity_a.categories = ['is_a']
    entity_b.categories = ['is_b']
    pair = CollidingPair(entity_a, entity_b)
    self.assertTrue(pair.has_control_categories('is_a', 'is_b'))
    self.assertTrue(pair.has_control_categories('is_b', 'is_a'))
    self.assertFalse(pair.has_control_categories('is_b', 'is_c'))

  def test_zaps_collide_with_entities(self):
    zap = Zap(0, 0)
    enemy = Enemy(0, 0)
    self.level.entities = [zap, enemy]
    self.collision_controller.handle_collisions(self.level.entities)
    self.assertFalse(zap in self.level.entities)
    self.assertFalse(enemy in self.level.entities)

  def test_get_collider_by_category(self):
    zap = Zap(0, 0)
    enemy = Enemy(0, 0)
    pair = CollidingPair(zap, enemy)
    self.assertEqual(zap, pair.get_collider_by_category('zap'))
