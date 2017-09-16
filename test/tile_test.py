import os
import sys
import unittest

sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from lib.tile import Tile

class TileTest(unittest.TestCase):

  def setUp(self):
    self.tile = Tile(2,3)

  def test_init(self):
    self.assertEqual(2, self.tile.location['x'])

  def test_set_type(self):
    self.tile.set_type("floor")
    self.assertEqual("floor", self.tile.type)

  def test_char(self):
    self.tile.type = "wall"
    self.assertEqual("#", self.tile.char())

  def test_color(self):
    self.assertEqual("BLACK", self.tile.color())

  def test_empty(self):
    self.assertTrue(self.tile.empty());
    self.tile.set_type("wall")
    print self.tile.empty
    self.assertFalse(self.tile.empty());

  def test_walkable(self):
    self.tile.set_type("floor")
    self.assertTrue(self.tile.walkable())
    self.tile.set_type("wall")
    self.assertFalse(self.tile.walkable())

if __name__ is '__main__':
  unittest.main()

