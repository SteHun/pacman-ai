class directions:
    up = 0
    down = 1
    left = 2
    right = 3
    no = 4
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
        self.maze_width_in_tiles = 28
        self.maze_height_in_tiles = 36
        with open("maze.txt", "r") as file:
            file_contents = file.read()
        for character in file_contents:
            if not character in (str(maze.wall), str(maze.empty), str(maze.dot), str(maze.power), "\n"):
                raise RuntimeError(f"it seems like the maze.txt file contains unsuppported character: '{character}'\nmake sure that the maze.txt file is correct")
                input()
                break
        file_contents = file_contents.splitlines()
        if False in [len(i) == len(file_contents[0]) for i in file_contents]:
            raise RuntimeError("it seems like the lines of the maze.txt file have an inconsistent length")
        if self.maze_width_in_tiles != len(file_contents[0]) or self.maze_height_in_tiles != len(file_contents):
            print(f"!WARNING!\nit seems like the dimentions of the maze.txt are different than expected:\ngot: {len(file_contents[0])}x{len(file_contents)}\nexpected: {self.maze_width_in_tiles}x{self.maze_height_in_tiles}\nthe game my not behave as expected\nmake sure that the maze.txt file is correct\npress ctrl+c to quit, or press enter to continue anyway")
            input()
        self.maze = [[int(b) for b in a] for a in file_contents]

        self.fps = 60
        self.tile_width_height = 8
        self.tile_to_left_of_fruit = (13,19)
        self.tile_to_right_of_fruit = (self.tile_to_left_of_fruit[0] + 1, self.tile_to_left_of_fruit[1])
        self.clock = 0
        #self.maze = [[maze.dot]*self.maze_width_in_tiles for _ in range(self.maze_height_in_tiles)] #create maze structure later
        self.input = directions.no
        self.player = Player(self)
        self.enemies = (Blinky(), Pinky(), Inky(), Clyde())
        self.active_fruit = fruits.none
        # self.tile_to_remove = 1 # DEBUG CODE FOR DOTS
        self.game_has_ended = False
        
        
        
    def set_input(self, key):
        assert key <= 4, f"input number should be between 1 and 4, not {key}"
        self.input = key
    def advance(self):
        if self.game_has_ended: return
        self.clock += 1
        self.player.advance()
        if self.player.amount_of_dots <= 0:
            self.game_has_ended = True
            return
        for enemy in self.enemies:
            enemy.advance()
        if self.clock % self.fps == 0:
            # DEBUG CODE FOR DOTS
            # self.maze[3][self.tile_to_remove] = maze.empty
            # if self.tile_to_remove < 26: self.tile_to_remove += 1

            for entity in self.enemies:# + (self.player,):
                entity.set_direction((self.clock // self.fps % 4))
            self.active_fruit = self.active_fruit + 1 if self.active_fruit < fruits.key else fruits.none

class Player:
    def __init__(self, game_object):
        self.game_object = game_object

        self.speed = 1.5 * 0.80 #This is the speed for level 1!
        
        self.amount_of_dots = 0
        for row in self.game_object.maze:
            for item in row:
                if item == maze.dot or item == maze.power:
                    self.amount_of_dots += 1

        self.x_tile_middle, self.y_tile_middle = 3.5, 3.5
        self.x_tile_pos = 14 
        self.y_tile_pos = 25
        self.x_pos_in_tile, self.y_pos_in_tile = 0, self.y_tile_middle
        self.x_pos = 8 * self.x_tile_pos + self.x_pos_in_tile
        self.y_pos = 8 * self.y_tile_pos + self.y_pos_in_tile
        self.max_x_pos = self.x_pos + 20
        self.max_y_pos = self.y_pos + 20
        self.min_x_pos = self.x_pos - 20
        self.min_y_pos = self.y_pos - 20

        self.options_for_moving = self.get_options_for_moving(self.game_object.maze, self.x_tile_pos, self.y_tile_pos)
        self.dont_move_next_frame = False

        self.direction = directions.up
        # DEBUG CODE
        # self.x_movement = 2
        # self.y_movement = 2
        # self.is_going_down_right = True
    
    def set_direction(self, direction):
        self.direction = direction
    
    def set_position(self, x_pos, y_pos):
        self.x_pos, self.y_pos = x_pos, y_pos
    
    def move(self, speed, direction):
        if direction == directions.up:
            self.y_pos_in_tile -= speed
            self.y_pos -= speed
        elif direction == directions.down:
            self.y_pos_in_tile += speed
            self.y_pos += speed
        elif direction == directions.left:
            self.x_pos_in_tile -= speed
            self.x_pos -= speed
        elif direction == directions.right:
            self.x_pos_in_tile += speed
            self.x_pos += speed
        
        while self.y_pos_in_tile >= self.game_object.tile_width_height:
            self.y_tile_pos += 1
            self.y_pos_in_tile -= self.game_object.tile_width_height
            return True
        while self.y_pos_in_tile <= 0:
            self.y_tile_pos -= 1
            self.y_pos_in_tile += self.game_object.tile_width_height
            return True
        while self.x_pos_in_tile >= self.game_object.tile_width_height:
            self.x_tile_pos += 1
            self.x_pos_in_tile -= self.game_object.tile_width_height
            return True
        while self.x_pos_in_tile <= 0:
            self.x_tile_pos -= 1
            self.x_pos_in_tile += self.game_object.tile_width_height
            return True
        return False
    
    def get_options_for_moving(self, maze_layout, x_pos, y_pos):
        options_for_moving = [False for i in range(4)]
        pass
        if x_pos <= 0 or x_pos >= len(maze_layout[0]) - 1:
            pass # this will be for when the player wraps around the screen, this is just a placeholder to prevent the game from chrashing
            return options_for_moving
        # going to the bottom edge of the screen or far out of bound will make this crash, but that should never happen, right?
        options_for_moving[directions.up] = maze_layout[y_pos - 1][x_pos] != maze.wall
        options_for_moving[directions.down] = maze_layout[y_pos + 1][x_pos] != maze.wall
        options_for_moving[directions.left] = maze_layout[y_pos][x_pos - 1] != maze.wall
        options_for_moving[directions.right] = maze_layout[y_pos][x_pos + 1] != maze.wall
        return options_for_moving
    
    def center_left_right(self):
        if abs(self.x_pos_in_tile - self.x_tile_middle) <= self.speed:
            self.x_pos_in_tile = self.x_tile_middle
            self.x_pos -= self.x_pos_in_tile - self.x_tile_middle
        elif self.x_pos_in_tile > self.x_tile_middle:
            self.x_pos_in_tile -= self.speed
            self.x_pos -= self.speed
        else:
            self.x_pos_in_tile += self.speed
            self.x_pos += self.speed
    
    def center_up_down(self):
        if abs(self.y_pos_in_tile - self.y_tile_middle) <= self.speed:
            self.y_pos_in_tile = self.y_tile_middle
            self.y_pos -= self.y_pos_in_tile - self.y_tile_middle
        elif self.y_pos_in_tile > self.y_tile_middle:
            self.y_pos_in_tile -= self.speed
            self.y_pos -= self.speed
        else:
            self.y_pos_in_tile += self.speed
            self.y_pos += self.speed

    def advance(self):
        if self.options_for_moving[self.game_object.input]: self.direction = self.game_object.input
        if self.dont_move_next_frame:
            self.dont_move_next_frame = False
            return
        if self.options_for_moving[self.direction]:
            tile_has_changed = self.move(self.speed, self.direction)
            if tile_has_changed:
                self.options_for_moving = self.get_options_for_moving(self.game_object.maze, self.x_tile_pos, self.y_tile_pos)
                if self.game_object.maze[self.y_tile_pos][self.x_tile_pos] == maze.dot:
                    self.game_object.maze[self.y_tile_pos][self.x_tile_pos] = maze.empty
                    self.amount_of_dots -= 1
                    self.dont_move_next_frame = True
                elif self.game_object.maze[self.y_tile_pos][self.x_tile_pos] == maze.power:
                    self.game_object.maze[self.y_tile_pos][self.x_tile_pos] = maze.empty
                    self.amount_of_dots -= 1
                    # TODO: add mechanism to give pacman power
            if self.y_pos_in_tile != self.y_tile_middle and (self.direction == directions.left or self.direction == directions.right):
                self.center_up_down()
            elif self.x_pos_in_tile != self.y_tile_middle and (self.direction == directions.up or self.direction == directions.down):
                self.center_left_right()
        elif self.x_pos_in_tile != self.x_tile_middle and (self.direction == directions.left or self.direction == directions.right):
            self.center_left_right()
        elif self.y_pos_in_tile != self.y_tile_middle and (self.direction == directions.up or self.direction == directions.down):
            self.center_up_down()
        
        self.x_pos = self.x_tile_pos * self.game_object.tile_width_height + self.x_pos_in_tile
        self.y_pos = self.y_tile_pos * self.game_object.tile_width_height + self.y_pos_in_tile


        #elif 

        # if self.is_going_down_right:
        #     if self.x_pos + self.x_movement >= self.max_x_pos or self.y_pos + self.y_movement >= self.max_y_pos:
        #         self.is_going_down_right = False
        #         self.advance()
        #         return
        #     self.x_pos += self.x_movement
        #     self.y_pos += self.y_movement
        # else:
        #     if self.x_pos - self.x_movement <= self.min_x_pos or self.y_pos - self.y_movement <= self.min_y_pos:
        #         self.is_going_down_right = True
        #         self.advance()
        #         return
        #     self.x_pos -= self.x_movement
        #     self.y_pos -= self.y_movement

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
