import os
import sys
import unittest
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from lib.level import *

class LevelTest(unittest.TestCase):

  def setUp(self):
    self.config = {
      "width": 40,
      "height": 20,
      "rooms": {
        "min_width": 3, "min_height": 3, "max_width": 11, "max_height": 5,
        "generation_attempts": 10
      },
    }

  def test_generates_(self):
    level = Level(self.config)
    self.assertEqual([], level.tiles)

class GeneratorTest(unittest.TestCase):

  def setUp(self):
    self.config = {
      "width": 40,
      "height": 20,
      "rooms": {
        "min_width": 3, "min_height": 3, "max_width": 11, "max_height": 5,
        "generation_attempts": 10
      },
    }

  def test_add_room_if_isolated(self):
    level = Level(self.config)
    generator = Generator(level, self.config)
    self.assertEqual(0, len(generator.rooms))
    room = Room(1, 1, 4, 4)
    generator.add_room_if_isolated(room)
    self.assertEqual(1, len(generator.rooms))
    room = Room(1, 1, 4, 4)
    generator.add_room_if_isolated(room)
    # the overlapping room is tossed out
    # so the room count does not change
    self.assertEqual(1, len(generator.rooms))


class RoomTest(unittest.TestCase):

  def test_collides_with_on_non_overlapping_room(self):
    room_a = Room(1, 1, 2, 2)
    room_b = Room(4, 4, 2, 2)
    self.assertFalse(room_a.collides_with(room_b))

  def test_collides_with_on_overlapping_room(self):
    room_a = Room(1, 1, 2, 2)
    room_b = Room(2, 2, 2, 2)
    self.assertTrue(room_a.collides_with(room_b))

if __name__ == '__main__':
  unittest.main()

