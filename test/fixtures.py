class Fixtures:

  level_config = {
      'width': 40,
      'height': 20,
      'rooms': {
        'min_width': 3, 'min_height': 3, 'max_width': 11, 'max_height': 5,
        'generation_attempts': 10
      },
    }

  game_config = {
      'game': {
        'levels': 3 
      },
      'level': {
        'width': 10,
        'height': 10,
        'rooms': {
          'min_width': 3, 'min_height': 3,
          'max_width': 3, 'max_height': 3,
          'generation_attempts': 10
        },
        'corridors': { 'dead_end_removals': 0 }
      },
      'windows': {
        'footer': {
          'width': 10,
          'height': 5
        }
      }
    }
