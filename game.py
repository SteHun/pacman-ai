class directions:
    up = 0
    down = 1
    left = 2
    right = 3
    no = 4


class game:
    def __init__(self):
        self.maze = None #add later
        self.input = directions.no
        self.player = player()
        self.enemies = (blinky(), pinky(), inky(), clyde())
    def set_input(self, key):
        if key > 4:
            raise RuntimeError("input numbers must be between 1 and 4")
        self.input = key
    def advance(self):
        pass

class player:
    def __init__(self):
        self.x_pos = 24
        self.y_pos = 24
        self.x_tile_pos = None #add later
        self.y_tile_pos = None #add later
        self.direction = directions.up
    def set_direction(self, direction):
        self.direction = direction
    def set_position(self, x_pos, y_pos):
        self.x_pos, self.y_pos = x_pos, y_pos

class enemy:
    def __init__(self):
        self.initialize()
    def initialize(self):
        self.x_tile_pos = None #add later
        self.y_tile_pos = None #add later
        self.direction = directions.up
    def set_direction(self, direction):
        self.direction = direction
    def set_position(self, x_pos, y_pos):
        self.x_pos, self.y_pos = x_pos, y_pos

class blinky(enemy):
    def __init__(self):
        self.initialize()
        self.x_pos = 40
        self.y_pos = 24

class pinky(enemy):
    def __init__(self):
        self.initialize()
        self.x_pos = 56
        self.y_pos = 24

class inky(enemy):
    def __init__(self):
        self.initialize()
        self.x_pos = 72
        self.y_pos = 24

class clyde(enemy):
    def __init__(self):
        self.initialize()
        self.x_pos = 88
        self.y_pos = 24
