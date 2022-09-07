from random import uniform

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
    cherry = 0
    berry = 1
    peach = 2
    apple = 3
    grape = 4
    galaxian = 5
    bell = 6
    key = 7
    none = 8
class modes:
    scatter = 0
    chase = 1



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
        self.input = directions.left
        self.player = Player(self)
        self.enemies = (Blinky(self), Pinky(self), Inky(self), Clyde(self))
        self.active_fruit = fruits.none
        self.fruit_to_appear = fruits.cherry
        self.fruit_apprearances = [self.player.amount_of_dots - 70, self.player.amount_of_dots - 170]
        self.fruits_have_been_eaten = False
        self.min_fruit_duration, self.max_fruit_duration = 9, 10
        # self.tile_to_remove = 1 # DEBUG CODE FOR DOTS
        self.game_has_ended = False
        
        
        
    def set_input(self, key):
        assert key <= 3, f"input number should be between 0 and 3, not {key}"
        self.input = key
    def advance(self):
        if self.game_has_ended: return
        self.clock += 1

        self.player.advance()
        if self.player.amount_of_dots <= 0:
            self.game_has_ended = True
            return
        elif not self.fruits_have_been_eaten and self.player.amount_of_dots == self.fruit_apprearances[0]:
            self.active_fruit = self.fruit_to_appear
            del self.fruit_apprearances[0]
            self.fruit_timer = self.clock + uniform(self.min_fruit_duration, self.max_fruit_duration) * 60
            if len(self.fruit_apprearances) == 0:   self.fruits_have_been_eaten = True
        if self.active_fruit != fruits.none and self.clock >= self.fruit_timer:
            self.active_fruit = fruits.none
        for enemy in self.enemies:
            enemy.advance()
        
        # if self.clock % self.fps == 0:
            # DEBUG CODE FOR DOTS
            # self.maze[3][self.tile_to_remove] = maze.empty
            # if self.tile_to_remove < 26: self.tile_to_remove += 1

            # for entity in self.enemies:# + (self.player,):
            #     entity.direction = self.clock // self.fps % 4
            # self.active_fruit = self.active_fruit + 1 if self.active_fruit < fruits.key else fruits.none

class Player:
    def __init__(self, game_object):
        self.game_object = game_object

        self.score = 0

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
        if x_pos <= 0 or x_pos >= len(maze_layout[0]) - 1:
            return [False, False, True, True]
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
                try:
                    if self.x_tile_pos < 0: raise IndexError
                    if self.game_object.maze[self.y_tile_pos][self.x_tile_pos] == maze.dot:
                        self.game_object.maze[self.y_tile_pos][self.x_tile_pos] = maze.empty
                        self.amount_of_dots -= 1
                        self.score += 10
                        self.dont_move_next_frame = True
                    elif self.game_object.maze[self.y_tile_pos][self.x_tile_pos] == maze.power:
                        self.game_object.maze[self.y_tile_pos][self.x_tile_pos] = maze.empty
                        self.amount_of_dots -= 1
                        self.score += 50
                        # TODO: add mechanism to give pacman power
                    elif (self.x_tile_pos, self.y_tile_pos) == self.game_object.tile_to_left_of_fruit or (self.x_tile_pos, self.y_tile_pos) == self.game_object.tile_to_right_of_fruit:
                        if self.game_object.active_fruit == fruits.cherry:
                            self.score += 100
                        elif self.game_object.active_fruit == fruits.berry:
                            self.score += 300
                        elif self.game_object.active_fruit == fruits.peach:
                            self.score += 500
                        elif self.game_object.active_fruit == fruits.apple:
                            self.score += 700
                        elif self.game_object.active_fruit == fruits.grape:
                            self.score += 1000
                        elif self.game_object.active_fruit == fruits.galaxian:
                            self.score += 2000
                        elif self.game_object.active_fruit == fruits.bell:
                            self.score += 3000
                        elif self.game_object.active_fruit == fruits.key:
                            self.score += 5000
                        self.game_object.active_fruit = fruits.none
                except IndexError:
                    if self.x_tile_pos == -2:   self.x_tile_pos = 28
                    elif self.x_tile_pos == 29: self.x_tile_pos = -1
                    
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
    def __init__(self, game_object):
        self.game_object = game_object
        self.setup_vars()
        self.x_tile_pos, self.y_tile_pos = 14, 13
        self.target_x, self.target_y = 2, 0
        self.initialize()

    def setup_vars(self):
        self.is_elroy_now = False
        self.is_second_elroy_now = False
        self.x_tile_middle, self.y_tile_middle = 3.5, 3.5
        self.direction = directions.up
        self.speed = 0.75 * 1.5
        self.target_x, self.target_y = self.scatter_target_x, self.scatter_target_y
        fps = self.game_object.fps
        self.is_frightened = False
        self.has_been_eaten = False
        self.next_mode = None
        self.mode_switch_times = [
            (7 * fps, modes.chase),
            (20 * fps, modes.scatter),
            (7 * fps, modes.chase),
            (20 * fps, modes.scatter),
            (5 * fps, modes.chase),
            (20 * fps, modes.scatter),
            (5 * fps, modes.chase)
            ]
        #self.mode_switch_times = [self.mode_switch_times[0]] + [(self.mode_switch_times[i][0] + self.mode_switch_times[i - 1][0], self.mode_switch_times[i][1]) for i in range(1, len(self.mode_switch_times))]
        time_to_add = 0
        for index, item in enumerate(self.mode_switch_times):
            self.mode_switch_times[index] = (item[0] + time_to_add, item[1])
            time_to_add = self.mode_switch_times[index][0]
        self.total_mode_switches = 0
        self.mode = modes.scatter
        self.switch_at_next_intersection = False
        self.is_in_house = False
        self.is_exiting_house = False
        self.house_exit_x_tile_pos, self.house_exit_y_tile_pos = 14, 13
        self.house_exit_x_pos_in_tile, self.house_exit_y_pos_in_tile = 0, self.y_tile_middle
        self.house_exit_x_pos, self.house_exit_y_pos = 112, 107.5


    def initialize(self):
        self.x_pos, self.y_pos = 8 * self.x_tile_pos + self.x_pos_in_tile, 8 * self.y_tile_pos + self.y_pos_in_tile
        self.next_direction = self.get_next_move(self.game_object.maze, self.x_tile_pos, self.y_tile_pos, self.target_x, self.target_y)
        self.direction = self.next_direction
        # self.max_x_pos, self.max_y_pos = self.x_pos + 20, self.y_pos + 20 # DEBUG CODE
        # self.min_x_pos, self.min_y_pos = self.x_pos - 20, self.y_pos - 20 # DEBUG CODE
        # self.x_movement, self.y_movement = 2, 2 # DEBUG CODE
        # self.is_going_down_right = True # DEBUG CODE
    def get_chase_target(self): return self.scatter_target_x, self.scatter_target_y

    def get_options_for_moving(self, maze_layout, x_pos, y_pos, restrict_up):
        #options_for_moving = [False for i in range(4)]
        options_for_moving = []
        if x_pos <= 0:# or x_pos >= len(maze_layout[0]) - 1:
            options_for_moving = [directions.left]
        elif x_pos >= len(maze_layout[0]) - 1:
            options_for_moving = [directions.right]
        # going to the bottom edge of the screen or far out of bound will make this crash, but that should never happen, right?
        else:
            if maze_layout[y_pos - 1][x_pos] != maze.wall and self.direction != directions.down and not restrict_up:  options_for_moving.append(directions.up)
            if maze_layout[y_pos + 1][x_pos] != maze.wall and self.direction != directions.up:  options_for_moving.append(directions.down)
            if maze_layout[y_pos][x_pos - 1] != maze.wall and self.direction != directions.right:  options_for_moving.append(directions.left)
            if maze_layout[y_pos][x_pos + 1] != maze.wall and self.direction != directions.left:  options_for_moving.append(directions.right)
        return options_for_moving
    
    def get_next_move(self, maze_layout, x_pos, y_pos, target_x, target_y, restrict_up = False):
        options_for_moving = self.get_options_for_moving(maze_layout, x_pos, y_pos, restrict_up)
        if len(options_for_moving) == 1:    return options_for_moving[0]
        target = (target_x, target_y)
        get_difference = lambda a, b: a - b if a >= b else b - a
        possible_positions = []
        for option in options_for_moving:
            if option == directions.up: possible_positions.append((x_pos, y_pos - 1))
            elif option == directions.down: possible_positions.append((x_pos, y_pos + 1))
            elif option == directions.left: possible_positions.append((x_pos - 1, y_pos))
            elif option == directions.right: possible_positions.append((x_pos + 1, y_pos))
        best_distance = None
        best_options = []
        for position, option in zip(possible_positions, options_for_moving):
            distance_vector = tuple([get_difference(position[i], target[i])**2 for i in range(2)])
            distance = sum(distance_vector)
            if best_distance == None or distance < best_distance:
                best_distance = distance
                best_options = [option]
            elif distance == best_distance:
                best_options.append(option)
        
        if len(best_options) == 1:
            return best_options[0]
        else:
            if directions.up in best_options:   return directions.up
            elif directions.left in best_options:   return directions.left
            elif directions.down in best_options:  return directions.down
            else:   return directions.right 

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

    def switch_direction(self):
        if self.direction == directions.up: self.direction = directions.down
        elif self.direction == directions.down: self.direction = directions.up
        elif self.direction == directions.left: self.direction = directions.right
        elif self.direction == directions.right: self.direction = directions.left

    def advance(self):
        if self.is_in_house:
            if not self.is_exiting_house and self.game_object.player.amount_of_dots <= self.dots_to_exit:
                self.is_exiting_house = True
                if self.x_pos + self.speed / 2 <= self.house_exit_x_pos:
                    self.direction = directions.right
                elif self.x_pos - self.speed / 2 >= self.house_exit_x_pos:
                    self.direction = directions.left
                else:
                    self.x_pos = self.house_exit_x_pos
                    self.direction = directions.up
            elif self.is_exiting_house:
                self.move(self.speed, self.direction)
                if self.direction != directions.up and (self.house_exit_x_pos - self.speed / 2 <= self.x_pos and self.house_exit_x_pos + self.speed / 2 >= self.x_pos):
                    self.direction = directions.up
                    self.x_pos = self.house_exit_x_pos
                elif self.direction == directions.up and (self.house_exit_y_pos + self.speed / 2 >= self.y_pos):
                    self.x_pos, self.y_pos = self.house_exit_x_pos, self.house_exit_y_pos
                    self.x_tile_pos, self.y_tile_pos = self.house_exit_x_tile_pos, self.house_exit_y_tile_pos
                    self.x_pos_in_tile, self.y_pos_in_tile = self.house_exit_x_pos_in_tile, self.house_exit_y_pos_in_tile
                    self.is_in_house = False
                    self.is_exiting_house = False
            return

        if self.elroy and not self.is_elroy_now and self.game_object.player.amount_of_dots == self.dots_for_elroy:
            print("elroy mode active!")
            self.is_elroy_now = True
            self.mode = modes.chase
            self.speed = self.first_elroy_speed
        elif self.elroy and not self.is_second_elroy_now and self.game_object.player.amount_of_dots == self.dots_for_second_elroy_speedup:
            print("second elroy mode active!")
            self.is_second_elroy_now = True
            self.speed = self.second_elroy_speed

        calculate_new_direction = self.move(self.speed, self.direction)
        if self.total_mode_switches < len(self.mode_switch_times) and self.game_object.clock == self.mode_switch_times[self.total_mode_switches][0]:
            calculate_new_direction = True
            if not self.is_elroy_now:
                self.mode = self.mode_switch_times[self.total_mode_switches][1]
                self.switch_direction()
            else:
                self.mode = modes.chase
            if self.mode == modes.scatter:  self.target_x, self.target_y = self.scatter_target_x, self.scatter_target_y
            self.total_mode_switches += 1



        if calculate_new_direction:
            if self.x_tile_pos == -2:   self.x_tile_pos = 28
            elif self.x_tile_pos == 29: self.x_tile_pos = -1
            if self.mode == modes.chase:    self.target_x, self.target_y = self.get_chase_target()
            if self.y_tile_pos == 16 and (self.x_tile_pos in range(-1, 6) or self.x_tile_pos in range(22, 29)):
                # change speed
                pass
            elif (self.y_tile_pos == 13 or self.y_tile_pos == 25) and self.x_tile_pos in range(10, 18):
                self.next_direction = self.get_next_move(self.game_object.maze, self.x_tile_pos, self.y_tile_pos, self.target_x, self.target_y, restrict_up=True)
            else:
                self.next_direction = self.get_next_move(self.game_object.maze, self.x_tile_pos, self.y_tile_pos, self.target_x, self.target_y)
            if self.next_direction != self.direction:
                self.switch_at_next_intersection = True
        if self.switch_at_next_intersection:
            if self.direction == directions.up and self.y_pos_in_tile <= self.y_tile_middle:
                self.y_pos_in_tile = self.y_tile_middle
                self.direction = self.next_direction
                self.switch_at_next_intersection = False
            elif self.direction == directions.down and self.y_pos_in_tile >= self.y_tile_middle:
                self.y_pos_in_tile = self.y_tile_middle
                self.direction = self.next_direction
                self.switch_at_next_intersection = False
            elif self.direction == directions.left and self.x_pos_in_tile <= self.x_tile_middle:
                self.y_pos_in_tile = self.y_tile_middle
                self.direction = self.next_direction
                self.switch_at_next_intersection = False
            elif self.direction == directions.right and self.x_pos_in_tile >= self.x_tile_middle:
                self.x_pos_in_tile = self.x_tile_middle
                self.direction = self.next_direction
                self.switch_at_next_intersection = False

        self.x_pos = self.x_tile_pos * self.game_object.tile_width_height + self.x_pos_in_tile
        self.y_pos = self.y_tile_pos * self.game_object.tile_width_height + self.y_pos_in_tile
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
    
class Blinky(Enemy):
    def __init__(self, game_object):
        self.game_object = game_object
        self.scatter_target_x, self.scatter_target_y = 25, 2
        self.elroy = True
        self.dots_for_elroy = 20
        self.dots_for_second_elroy_speedup = 10
        self.first_elroy_speed = 0.80 * 1.5
        self.second_elroy_speed = 0.85 * 1.5
        self.setup_vars()
        self.x_tile_pos, self.y_tile_pos = 14, 13
        self.x_pos_in_tile, self.y_pos_in_tile = 0, self.y_tile_middle
        self.initialize()
    def get_chase_target(self):
        return self.game_object.player.x_tile_pos, self.game_object.player.y_tile_pos

class Pinky(Enemy):
    def __init__(self, game_object):
        self.game_object = game_object
        self.scatter_target_x, self.scatter_target_y = 3, 2
        self.elroy = False
        self.setup_vars()
        self.x_tile_pos, self.y_tile_pos = 14, 16
        self.x_pos_in_tile, self.y_pos_in_tile = 0, self.y_tile_middle
        self.is_in_house = True
        self.dots_to_exit = self.game_object.player.amount_of_dots - 0
        self.initialize()
    def get_chase_target(self):
        player_direction = self.game_object.player.direction
        player_x_pos, player_y_pos = self.game_object.player.x_tile_pos, self.game_object.player.y_tile_pos
        if player_direction == directions.up:
            return player_x_pos - 4, player_y_pos - 4
        elif player_direction == directions.down:
            return player_x_pos, player_y_pos + 4
        elif player_direction == directions.left:
            return player_x_pos - 4, player_y_pos
        else:
            return player_x_pos + 4, player_y_pos
        

class Inky(Enemy):
    def __init__(self, game_object):
        self.game_object = game_object
        self.scatter_target_x, self.scatter_target_y = 3, 2
        self.elroy = False
        self.setup_vars()
        self.x_tile_pos, self.y_tile_pos = 12, 16
        self.x_pos_in_tile, self.y_pos_in_tile = 0, self.y_tile_middle
        self.is_in_house = True
        self.dots_to_exit = self.game_object.player.amount_of_dots - 10
        self.initialize()
    def get_chase_target(self):
        return self.game_object.player.x_tile_pos, self.game_object.player.y_tile_pos

class Clyde(Enemy):
    def __init__(self, game_object):
        self.game_object = game_object
        self.scatter_target_x, self.scatter_target_y = 3, 2
        self.elroy = False
        self.setup_vars()
        self.x_tile_pos, self.y_tile_pos = 16, 16
        self.x_pos_in_tile, self.y_pos_in_tile = 0, self.y_tile_middle
        self.is_in_house = True
        self.dots_to_exit = self.game_object.player.amount_of_dots - 20
        self.initialize()
    def get_chase_target(self):
        return self.game_object.player.x_tile_pos, self.game_object.player.y_tile_pos
