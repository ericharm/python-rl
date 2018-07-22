import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.entity import *
from src.level import Level
from test.fixtures import Fixtures

class EntityTest(unittest.TestCase):

  def setUp(self):
    self.config = Fixtures.level_config

  def setup_level(self):
    level = Level(self.config).create_empty_tiles()
    for x in range(0, level.width):
      for y in range(0, level.height):
        level.tiles[x][y].set_type('floor')
    for column in level.tiles:
      level.flattened_tiles.extend(column)
    return level

  # Entity
  def test_distance_from(self):
    hero = Hero(2, 5)
    enemy = Enemy(5,9)
    self.assertEqual(5, hero.distance_from_entity(enemy))

  def test_default_update_just_returns_true(self):
    self.assertTrue(Entity(0,0).update(Level(self.config)))

  def test_default_char_is_a_blank_space(self):
    self.assertEqual(' ', Entity(0,0).char())

  def test_move_entity(self):
    level = Level(self.config).create_empty_tiles()
    level.tiles[0][0].set_type('floor')
    level.tiles[1][0].set_type('floor')
    entity = Entity(0, 0)
    entity.move(1, 0, level)
    self.assertEqual((1, 0), (entity.x, entity.y))

  def test_move_entity_gets_stuck_on_unwalkable_tile(self):
    level = Level(self.config).create_empty_tiles()
    level.tiles[0][0].set_type('floor')
    entity = Entity(0, 0)
    entity.move(1, 0, level)
    self.assertEqual((0, 0), (entity.x, entity.y))

  def test_set_hero_state(self):
    self.assertEqual('moving', Hero(0, 0).set_state('moving').state)

  def test_hero_char(self):
    self.assertEqual('@', Hero(0, 0).char())

  def test_is_colliding_with(self):
    chuck = Entity(1, 1)
    larry = Entity(1, 2)
    seymour = Entity(1, 2)
    self.assertTrue(larry.is_colliding_with(seymour))
    self.assertFalse(chuck.is_colliding_with(larry))

  def test_colliding_entities(self):
    chuck = Entity(1, 1)
    larry = Entity(1, 2)
    seymour = Entity(1, 2)
    self.assertEqual(1, len(larry.colliding_entities([chuck, larry, seymour])))
    self.assertEqual(0, len(chuck.colliding_entities([chuck, larry, seymour])))


  # Hero
  def test_hero_initial_state_is_moving(self):
    hero = Hero(1, 2)
    self.assertEqual("moving", hero.state)

  def test_decrement_hero_zaps(self):
    hero = Hero(0, 0)
    zaps = reduce(lambda a, b: a if a['name'] is 'Zapgun Charges' else b, hero.inventory)
    quantity = zaps['quantity']
    hero.decrement_zaps()
    self.assertEqual(quantity - 1, zaps['quantity'])

  # Enemy
  def update_new_enemy(self, enemy, hero):
    level = self.setup_level()
    enemy = Enemy(enemy.x, enemy.y)
    level.entities = [Hero(hero.x, hero.y), enemy]
    enemy.update(level)
    return (enemy.x, enemy.y)

  def test_in_acting_range(self):
    hero = Hero(0, 0)
    enemy = Enemy(5, 0)
    enemy.acting_range = 4
    self.assertFalse(enemy.in_acting_range(hero))
    enemy.acting_range = 5
    self.assertTrue(enemy.in_acting_range(hero))

  def test_enemy_char(self):
    self.assertEqual('a', Enemy(0, 0).char())

  def test_enemy_finds_path_to_hero(self):
    level = self.setup_level()
    enemy = Enemy(1, 0)
    hero = Hero(5, 0)
    enemy.move(hero, level)
    self.assertEqual((2, 0), (enemy.x, enemy.y))

  def test_enemy_tries_only_paths_of_reasonable_distance(self):
    level = self.setup_level()
    enemy = Enemy(1, 0)
    hero = Hero(34, 0)
    level.entities = [hero, enemy]
    enemy.move(hero, level)
    self.assertEqual((1, 0), (enemy.x, enemy.y))

  # Zaps
  def test_handle_entity_collisions(self):
    level = self.setup_level()
    enemy = Enemy(6, 5)
    zap = Zap(5, 5)
    zap.set_velocity(0, 0)
    level.entities = [zap, enemy]
    enemy.x -= 1
    level.update()
    self.assertEqual((5, 5), (zap.x, zap.y))
    self.assertEqual(0, len(level.entities))

  def test_zap_hits_a_wall(self):
    level = self.setup_level()
    zap = Zap(5, 5)
    level.tiles[6][5].set_type('wall')
    level.entities = [zap]
    zap.set_velocity(1, 0)
    level.update()
    self.assertEqual(0, len(level.entities))

