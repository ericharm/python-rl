import os
import sys
import unittest

sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from src.util import *

class UtilTest(unittest.TestCase):

  def test_vector_to_binary(self):
    vector = Vector(5, 5).to_binary()
    self.assertEqual((1, 1), (vector.x, vector.y))
    vector = Vector(5, 0).to_binary()
    self.assertEqual((1, 0), (vector.x, vector.y))
    vector = Vector(-5, 5).to_binary()
    self.assertEqual((-1, 1), (vector.x, vector.y))
    vector = Vector(0, -2).to_binary()
    self.assertEqual((0, -1), (vector.x, vector.y))

  def test_flip_coin(self):
    flips = map(lambda flip: Chance.flip_coin(), range(0, 10))
    self.assertTrue(False in flips)
    self.assertTrue(True in flips)
