import os
import sys
import unittest
import curses

sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.tile import Tile

class TileTest(unittest.TestCase):

  def setUp(self):
    self.tile = Tile(2,3)

  def test_init(self):
    self.assertEqual(2, self.tile.x)

  def test_set_type(self):
    self.tile.set_type("floor")
    self.assertEqual("floor", self.tile.type)

  def test_char(self):
    self.tile.type = "corridor"
    self.assertEqual("#", self.tile.char())

  def test_empty(self):
    self.assertTrue(self.tile.empty());
    self.tile.set_type("wall")
    self.assertFalse(self.tile.empty());

  def test_walkable(self):
    self.tile.set_type("floor")
    self.assertTrue(self.tile.walkable())
    self.tile.set_type("wall")
    self.assertFalse(self.tile.walkable())

  def test_odd(self):
    even_tile = Tile(2,2)
    odd_tile = Tile(3,3)
    mixed_tile = Tile(2,3)
    self.assertFalse(even_tile.odd())
    self.assertTrue(odd_tile.odd())
    self.assertFalse(mixed_tile.odd())

  def test_at_distance(self):
    horizontally_aligned_tile = Tile(10, 3)
    vertically_aligned_tile = Tile(2, 10)
    diagonally_aligned_tile = Tile(3, 4)
    self.assertFalse(self.tile.at_distance(7, horizontally_aligned_tile))
    self.assertTrue(self.tile.at_distance(8, horizontally_aligned_tile))
    self.assertTrue(self.tile.at_distance(7,vertically_aligned_tile))
    self.assertFalse(self.tile.at_distance(8, vertically_aligned_tile))
    self.assertFalse(self.tile.at_distance(1, diagonally_aligned_tile))

  def test_direction_from(self):
    south_east_tile = Tile(5,5)
    west_tile = Tile(1,3)
    north_east_tile = Tile(5,2)
    self.assertEqual(south_east_tile.direction_from(self.tile), (1,1))
    self.assertEqual(west_tile.direction_from(self.tile), (-1,0))
    self.assertEqual(north_east_tile.direction_from(self.tile), (1,-1))

  def test_dead_end(self):
    tile = Tile(2,2)
    west = Tile(1,2)
    east = Tile(3,2)
    north = Tile(2,1)
    south = Tile(2,3)
    tile.set_type("corridor")
    south.set_type("corridor")
    adjacents = [west, east, north, south]
    self.assertTrue(tile.dead_end(adjacents))

  def test_not_dead_end(self):
    tile = Tile(2,2)
    west = Tile(1,2)
    east = Tile(3,2)
    north = Tile(2,1)
    south = Tile(2,3)
    tile.set_type("corridor")
    south.set_type("corridor")
    north.set_type("corridor")
    adjacents = [west, east, north, south]
    self.assertFalse(tile.dead_end(adjacents))


if __name__ is '__main__':
  unittest.main()

