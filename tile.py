class Tile:

    def __init__(self, x, y):
        self.type = "empty"
        self.location = {"x": x, "y": y}
        self.revealed = False
        self.visible = False
        self.in_periphery = False

    def char(self):
        if self.type == "floor":
            return "+"
        elif self.type == "wall":
            return "="
        elif self.type == "empty":
            return " "

    def color(self):
        if self.visible:
            return "BRIGHT_WHITE"
        elif self.in_periphery:
            return "WHITE"
        elif self.revealed:
            return "GRAY"
        else:
            return "BLACK"

    def set_type(self, new_type):
        self.type = new_type

    def draw(self, screen):
          screen.addstr(self.location['y'], self.location['x'], self.char())

