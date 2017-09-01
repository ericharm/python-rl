from curses import *
import yaml
from lib.game import Game

with open("config/config.yml", 'r') as stream:
  try:
    config = yaml.load(stream)
  except yaml.YAMLError as exc:
    print(exc)


def main(stdscr):
  game = Game(config)
  game.run(stdscr)

wrapper(main)

