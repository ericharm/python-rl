import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.level import *

class LevelTest(unittest.TestCase):

  def floor_tile_count(self):
    floor_tiles = []
    for column in range(0, self.config['width']):
      for row in range(0, self.config['height']):
        if self.level.tiles[column][row].type is "floor":
          floor_tiles.append(True)
    return len(floor_tiles)

  def setUp(self):
    self.config = {
      'width': 40,
      'height': 20,
      'rooms': {
        'min_width': 3, 'min_height': 3, 'max_width': 11, 'max_height': 5,
        'generation_attempts': 10
      },
    }
    self.level = Level(self.config)
    self.level.create_empty_tiles()

  def test_level_initializes_without_tiles(self):
    level = Level(self.config)
    self.assertEqual([], level.tiles)

  def test_level_creates_empty_tiles(self):
    level = Level(self.config)
    level.create_empty_tiles()
    self.assertEqual(len(level.tiles), self.config['width'])
    self.assertEqual(len(level.tiles[0]), self.config['height'])

  def test_generator_generates_rooms(self):
    self.assertEqual(0, len(self.level.rooms))
    self.level.generate_rooms()
    self.assertGreater(len(self.level.rooms), 0,
                       "Generator should have created at least one room")

  def test_level_inserts_rooms(self):
    tiles = self.level.tiles
    self.assertEqual(0, self.floor_tile_count())
    self.level.generate_rooms()
    self.level.insert_rooms()
    self.assertGreater(self.floor_tile_count(), 0)

  def test_generator_gets_odd_numbers(self):
    number = self.level.odd_number(1,100)
    self.assertFalse(number % 2 is 0)

  def test_room_does_not_collide_with_isolated_room(self):
    room_a = Room(1, 1, 2, 2)
    room_b = Room(4, 4, 2, 2)
    self.assertFalse(room_a.collides_with_room(room_b))

  def test_room_collides_with_overlapping_room(self):
    room_a = Room(1, 1, 2, 2)
    room_b = Room(2, 2, 2, 2)
    self.assertTrue(room_a.collides_with_room(room_b))

  def test_room_not_within_level_with_width_beneath_room_x(self):
    room = Room (10, 10, 2, 2)
    level = Level(self.config)
    level.width = 9
    self.assertFalse(room.within_level(level))

  def test_room_within_level_with_width_above_room_x_plus_room_width(self):
    room = Room (10, 10, 2, 2)
    level = Level(self.config)
    level.width = 13
    self.assertTrue(room.within_level(level))

  def test_get_random_floor_tile(self):
    self.level.generate_rooms()
    self.level.insert_rooms()
    tile = self.level.get_random_floor_tile()
    self.assertEqual(tile.type, "floor")

  def test_connect_neighbors_as_corridor(self):
    source_tile = self.level.tiles[1][1]
    target_tile = self.level.tiles[3][1]
    inbetween_tile = self.level.tiles[2][1]
    self.level.connect_neighbors_as_corridor(source_tile, target_tile)
    self.assertEqual(source_tile.type, "corridor");
    self.assertEqual(target_tile.type, "corridor");
    self.assertEqual(inbetween_tile.type, "corridor");

