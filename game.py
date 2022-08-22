class directions:
    up = 1
    down = 2
    left = 3
    right = 4
    no = 0
class maze:
    wall = 0
    empty = 1
    dot = 2
    power = 3
class fruits:
    none = 0
    cherry = 1
    berry = 2
    peach = 3
    apple = 4
    grape = 5
    galaxian = 6
    bell = 7
    key = 8



class Game:
    def __init__(self):
        self.fps = 60
        self.maze_width_in_tiles = 28
        self.maze_height_in_tiles = 36
        self.tile_width_height = 8
        self.tile_to_left_of_fruit = (13,19)
        self.tile_to_right_of_fruit = (self.tile_to_left_of_fruit[0] + 1, self.tile_to_left_of_fruit[1])
        self.clock = 0
        #self.maze = [[maze.dot]*self.maze_width_in_tiles for _ in range(self.maze_height_in_tiles)] #create maze structure later
        self.input = directions.no
        self.player = Player()
        self.enemies = (Blinky(), Pinky(), Inky(), Clyde())
        self.active_fruit = fruits.none
        self.tile_to_remove = 1 #debug: remove later
        with open("maze.txt", "r") as file:
            file_contents = file.read()
        for character in file_contents:
            if not character in (str(maze.wall), str(maze.empty), str(maze.dot), str(maze.power), "\n"):
                print(f"!WARNING!\nit seems like the maze.txt file contains unsuppported character: '{character}'\nthe game will interpret these as empty spaces\nmake sure that the maze.txt file is correct\npress ctrl+c to quit, or press enter to continue anyway")
                input()
                break
        file_contents = file_contents.splitlines()
        if False in [len(i) == len(file_contents[0]) for i in file_contents]:
            raise RuntimeError("it seems like the lines of the maze.txt file have an inconsistent length")
        if self.maze_width_in_tiles != len(file_contents[0]) or self.maze_height_in_tiles != len(file_contents):
            print(f"!WARNING!\nit seems like the dimentions of the maze.txt are different than expected:\ngot: {len(file_contents[0])}x{len(file_contents)}\nexpected: {self.maze_width_in_tiles}x{self.maze_height_in_tiles}\nthe game my not behave as expected\nmake sure that the maze.txt file is correct\npress ctrl+c to quit, or press enter to continue anyway")
            input()
        self.maze = [[b for b in a] for a in file_contents]
        
        
        
    def set_input(self, key):
        assert key <= 4, f"input number should be between 1 and 4, not {key}"
        self.input = key
    def advance(self):
        self.clock += 1
        self.player.advance()
        for enemy in self.enemies:
            enemy.advance()
        if self.clock % self.fps == 0:
            self.maze[3][self.tile_to_remove] = maze.empty
            if self.tile_to_remove < 26: self.tile_to_remove += 1

            for entity in (self.player,) + self.enemies:
                entity.set_direction((self.clock // self.fps % 4) + 1)
            self.active_fruit = self.active_fruit + 1 if self.active_fruit < fruits.key else fruits.none

class Player:
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

class Enemy:
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

class Blinky(Enemy):
    def __init__(self):
        self.x_pos = 40
        self.y_pos = 24
        self.initialize()

class Pinky(Enemy):
    def __init__(self):
        self.x_pos = 56
        self.y_pos = 24
        self.initialize()

class Inky(Enemy):
    def __init__(self):
        self.x_pos = 72
        self.y_pos = 24
        self.initialize()

class Clyde(Enemy):
    def __init__(self):
        self.x_pos = 88
        self.y_pos = 24
        self.initialize()
