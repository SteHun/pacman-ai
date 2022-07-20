class directions:
    up = 1
    down = 2
    left = 3
    right = 4
    no = 0


class game:
    def __init__(self):
        self.fps = 60
        self.maze_width_in_tiles = 28
        self.maze_height_in_tiles = 36
        self.tile_width_height = 8
        self.clock = 0
        self.maze = None #add later
        self.eaten_dots = [[False]*self.maze_width_in_tiles for _ in range(self.maze_height_in_tiles)]
        self.input = directions.no
        self.player = player()
        self.enemies = (blinky(), pinky(), inky(), clyde())
        self.tile_to_remove = 1 #debug: remove later
    def set_input(self, key):
        assert key <= 4, f"input number should be between 1 and 4, not {key}"
        self.input = key
    def advance(self):
        self.clock += 1
        self.player.advance()
        for enemy in self.enemies:
            enemy.advance()
        if self.clock % self.fps == 0:
            self.eaten_dots[4][self.tile_to_remove] = True
            if self.tile_to_remove < 26: self.tile_to_remove += 1

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
