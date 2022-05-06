from queue import Queue


class Pather:
    def __init__(self, source, level):
        self.grid = level.tiles
        self.flattened_tiles = level.flattened_tiles
        self.frontier = Queue()
        self.frontier.put(source)
        self.paths = {}
        self.paths[source] = []

    def get_path(self, goal):
        while not self.frontier.empty():
            current = self.frontier.get()

            if current == goal:
                return self.paths[current]

            for tile in current.get_walkable_neighbors(self.flattened_tiles):
                if tile not in self.paths:
                    self.frontier.put(tile)
                    path = list(self.paths[current])
                    path.append((tile.x, tile.y))
                    if len(path) > 15:
                        return []
                    self.paths[tile] = path
