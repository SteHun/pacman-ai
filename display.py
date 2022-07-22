import sys, pygame
import game
from os import path
from time import time, sleep

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#MAKE SURE TO MULTIPLY POSITIONS BY SIZE_MULTIPLIER WHEN FINALIZING
class Window:
    def __init__(self, game_object, size_multiplier=2):
        pygame.init()
        self.game_object = game_object
        self.size_multiplier = size_multiplier

        self.sprite_width_length = 16
        self.width = 224
        self.height = 288
        number_of_sprites_per_enemy_type = 4
        scared_blue_enemy_sprite_position = (0, 4)
        scared_white_enemy_sprite_position = (1, 4)


        self.size = self.width, self.height = self.width*self.size_multiplier, self.height*self.size_multiplier

        self.screen = pygame.display.set_mode(self.size)

        #lambdas
        enlarge_image = lambda image, factor : pygame.transform.scale(image, (image.get_width()*factor, image.get_height()*factor))
        get_rect = lambda x_cord, y_cord : (self.sprite_width_length*x_cord*self.size_multiplier, self.sprite_width_length*y_cord*self.size_multiplier, self.sprite_width_length*self.size_multiplier, self.sprite_width_length*self.size_multiplier)
        self.scale_position = lambda x_pos, y_pos : tuple([i * self.size_multiplier for i in (x_pos, y_pos)])

        #load background
        self.bg = pygame.image.load(path.join("images", "maze.png"))
        self.bg = enlarge_image(self.bg, self.size_multiplier).convert()


        #load player
        player_right = enlarge_image(pygame.image.load(path.join("images", "pacman.png")), self.size_multiplier)
        player_up = pygame.transform.rotate(player_right, 90)
        player_left = pygame.transform.rotate(player_up, 90)
        player_down = pygame.transform.flip(player_up, False, True)
        self.player_sprites = (player_up, player_down, player_left, player_right)

        #load enemies
        self.enemy_sheet = enlarge_image(pygame.image.load(path.join("images", "enemies.png")), self.size_multiplier)

        self.blinky_rects = tuple([get_rect(i, 0) for i in range(number_of_sprites_per_enemy_type)])
        self.pinky_rects = tuple([get_rect(i, 1) for i in range(number_of_sprites_per_enemy_type)])
        self.inky_rects = tuple([get_rect(i, 2) for i in range(number_of_sprites_per_enemy_type)])
        self.clyde_rects = tuple([get_rect(i, 3) for i in range(number_of_sprites_per_enemy_type)])

        self.scared_blue_rect = get_rect(*scared_blue_enemy_sprite_position)
        self.scared_white_rect = get_rect(*scared_white_enemy_sprite_position)

    def refresh(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.player_sprites[self.game_object.player.direction - 1], self.scale_position(self.game_object.player.x_pos, self.game_object.player.y_pos))
        #!ENEMY BLITTING UNFINISHED!#
        #!ENEMIES WILL NEVER BE SCARED/SCARED WHITE!#
        for enemy in self.game_object.enemies:
            if type(enemy) == game.Blinky:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.blinky_rects[enemy.direction - 1])
            elif type(enemy) == game.Pinky:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.pinky_rects[enemy.direction - 1])
            elif type(enemy) == game.Inky:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.inky_rects[enemy.direction - 1])
            elif type(enemy) == game.Clyde:
                self.screen.blit(self.enemy_sheet, self.scale_position(enemy.x_pos, enemy.y_pos), area=self.clyde_rects[enemy.direction - 1])

        pygame.display.flip()
    

if __name__ == "__main__":
    frame_duration = 1/60
    game_instance = game.Game()
    window_instance = Window(game_instance, size_multiplier=2)
    while 1:
        start_time = time()
        window_instance.refresh()
        game_instance.advance()
        sleep(max(0, frame_duration - (time() - start_time)))

#:ADD THIS STUFF TO DEBUG GRAPHICS:#
# self.screen.blit(self.test_ball, self.test_ball_rect)
# self.screen.blit(self.player_sprites[0], (20, 20))
# self.screen.blit(self.player_sprites[1], (20, 50))
# self.screen.blit(self.player_sprites[2], (20, 80))
# self.screen.blit(self.player_sprites[3], (20, 110))
# for enemy_index, enemy in enumerate((self.blinky_rects, self.pinky_rects, self.inky_rects, self.clyde_rects)):
#     for rect_index, rect in enumerate(enemy):
#         self.screen.blit(self.enemy_sheet, (50*enemy_index+50, 30*rect_index+20), area=rect)
#self.screen.blit(self.enemy_sheet, (250, 20), area=self.scared_blue_rect)
#self.screen.blit(self.enemy_sheet, (250, 50), area=self.scared_white_rect)