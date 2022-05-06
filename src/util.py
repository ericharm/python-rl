import math
import random
import curses


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def to_binary(self):
        coords = list(
            map(lambda value: 0 if value == 0 else value / abs(value), [self.x, self.y])
        )
        self.x = coords[0]
        self.y = coords[1]
        return self

    def in_level(self, level):
        return self.x < level.width and self.y < level.height


class Chance:
    @staticmethod
    def flip_coin():
        return random.choice([True, False])


class Color:
    colors = {
        "black": 1,
        "green": 2,
        "blue": 3,
        "red": 4,
        "magenta": 5,
        "white": 6,
        "yellow": 7,
    }

    @staticmethod
    def use(color):  # pragma: no cover
        return curses.color_pair(Color.colors[color])
