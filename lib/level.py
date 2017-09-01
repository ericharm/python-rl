from tile import Tile

class Level:

    def __init__(self, width, height):
        self.tiles = []
        self.width = width
        self.height = height
        self.create_tiles()

    def create_tiles(self):
        for x in range(0,self.width):
            self.tiles.append([])
            for y in range(0,self.height):
                self.tiles[x].append(None)
                tile = Tile(x,y)
                self.tiles[x][y] = tile

    def draw(self, screen):
        for x in range(0,self.width):
            for y in range(0,self.height):
                self.tiles[x][y].draw(screen)

