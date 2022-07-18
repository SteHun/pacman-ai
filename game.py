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
        self.player.advance()
        for enemy in self.enemies:
            enemy.advance()

class player:
    def __init__(self):
        self.x_pos = 24
        self.y_pos = 24
        self.max_x_pos = 44
        self.max_y_pos = 44
        self.min_x_pos = 4
        self.min_y_pos = 4
        self.x_movement = 2
        self.y_movement = 2
        self.is_going_down_right = True
        self.x_tile_pos = None #add later
        self.y_tile_pos = None #add later
        self.direction = directions.up
    
    def set_direction(self, direction):
        self.direction = direction
    
    def set_position(self, x_pos, y_pos):
        self.x_pos, self.y_pos = x_pos, y_pos

    def advance(self):
        if self.is_going_down_right:
            if self.x_pos + self.x_movement >= self.max_x_pos or self.y_pos + self.y_movement >= self.max_y_pos:
                self.is_going_down_right = False
                self.advance()
                return
            self.x_pos += self.x_movement
            self.y_pos += self.y_movement
        else:
            if self.x_pos - self.x_movement <= self.min_x_pos or self.y_pos - self.y_movement <= self.min_y_pos:
                self.is_going_down_right = True
                self.advance()
                return
            self.x_pos -= self.x_movement
            self.y_pos -= self.y_movement

class enemy:
    def __init__(self):
        self.initialize()

    def initialize(self):
        self.x_tile_pos = None #add later
        self.y_tile_pos = None #add later
        self.max_x_pos, self.max_y_pos = self.x_pos + 20, self.y_pos + 20
        self.min_x_pos, self.min_y_pos = self.x_pos - 20, self.y_pos - 20
        self.x_movement, self.y_movement = 2, 2
        self.is_going_down_right = True
        self.direction = directions.up

    def set_direction(self, direction):
        self.direction = direction

    def set_position(self, x_pos, y_pos):
        self.x_pos, self.y_pos = x_pos, y_pos
    
    def advance(self):
        if self.is_going_down_right:
            if self.x_pos + self.x_movement >= self.max_x_pos or self.y_pos + self.y_movement >= self.max_y_pos:
                self.is_going_down_right = False
                self.advance()
                return
            self.x_pos += self.x_movement
            self.y_pos += self.y_movement
        else:
            if self.x_pos - self.x_movement <= self.min_x_pos or self.y_pos - self.y_movement <= self.min_y_pos:
                self.is_going_down_right = True
                self.advance()
                return
            self.x_pos -= self.x_movement
            self.y_pos -= self.y_movement

class blinky(enemy):
    def __init__(self):
        self.x_pos = 40
        self.y_pos = 24
        self.initialize()

class pinky(enemy):
    def __init__(self):
        self.x_pos = 56
        self.y_pos = 24
        self.initialize()

class inky(enemy):
    def __init__(self):
        self.x_pos = 72
        self.y_pos = 24
        self.initialize()

class clyde(enemy):
    def __init__(self):
        self.x_pos = 88
        self.y_pos = 24
        self.initialize()
