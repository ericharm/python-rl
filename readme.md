A simple roguelike featuring procedural level generation, player inventory, path finding

## Up and running
- `git clone https://github.com/ericharm/python-rl.git`
- `cd python-rl`
- `pip install -r requirements.txt`
- if your version of python does not include the curses library you may need to install it manually
- `python init.py`

## Tests
- `pytest test/`

### Coverage
- `pytest --cov=src test`
