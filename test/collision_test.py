import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.collision_controller import *
from src.entity import *

class CollisionTest(unittest.TestCase):

  def setUp(self):
    self.collision_controller = CollisionController()

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
    self.collision_controller.handle_collisions([zap, enemy])
    self.assertTrue('slated-for-removal' in zap.categories)
    self.assertTrue('slated-for-removal' in enemy.categories)

  def test_get_collider_by_category(self):
    zap = Zap(0, 0)
    enemy = Enemy(0, 0)
    pair = CollidingPair(zap, enemy)
    self.assertEqual(zap, pair.get_collider_by_category('zap'))
