import sys, pygame
import game
from os import path
from time import time, sleep

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#MAKE SURE TO MULTIPLY POSITIONS BY SIZE_MULTIPLIER WHEN FINALIZING
class Window:
    def __init__(self, game_object, size_multiplier=2):
        pygame.init()
        self.sprite_width_length = 16
        self.width = 224
        self.height = 288
        self.ball_speed = [2, 2]

        self.game_object = game_object
        self.size_multiplier = size_multiplier

        self.size = self.width, self.height = self.width*self.size_multiplier, self.height*self.size_multiplier

        self.screen = pygame.display.set_mode(self.size)

        #lambdas
        enlarge_image = lambda image, factor : pygame.transform.scale(image, (image.get_width()*factor, image.get_height()*factor))
        get_rect = lambda x_cord, y_cord : (self.sprite_width_length*x_cord*self.size_multiplier, self.sprite_width_length*y_cord*self.size_multiplier, self.sprite_width_length*self.size_multiplier, self.sprite_width_length*self.size_multiplier)
        

        #load background
        self.bg = pygame.image.load(path.join("images", "maze.png"))
        self.bg = enlarge_image(self.bg, self.size_multiplier).convert()

        #load ball
        self.test_ball = pygame.image.load(path.join("images", "test_ball.gif"))
        #ball = enlarge_image(self.ball, self.size_multiplier)
        self.test_ball_rect = self.test_ball.get_rect()

        #load player
        self.player_right = enlarge_image(pygame.image.load(path.join("images", "pacman.png")), self.size_multiplier)
        self.player_up = pygame.transform.rotate(self.player_right, 90)
        self.player_left = pygame.transform.rotate(self.player_up, 90)
        self.player_down = pygame.transform.flip(self.player_up, False, True)

        #load enemies
        self.enemy_sheet = enlarge_image(pygame.image.load(path.join("images", "enemies.png")), self.size_multiplier)

        self.blinky_rect = tuple([get_rect(i, 0) for i in range(4)])
        self.pinky_rect = tuple([get_rect(i, 1) for i in range(4)])
        self.inky_rect = tuple([get_rect(i, 2) for i in range(4)])
        self.clyde_rect = tuple([get_rect(i, 3) for i in range(4)])

        self.scared_blue_rect = get_rect(0, 4)
        self.scared_white_rect = get_rect(1, 4)

    def refresh(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()


        self.test_ball_rect = self.test_ball_rect.move(self.ball_speed)

        if self.test_ball_rect.left < 0 or self.test_ball_rect.right > self.width:
            self.ball_speed[0] = -self.ball_speed[0]

        if self.test_ball_rect.top < 0 or self.test_ball_rect.bottom > self.height:
            self.ball_speed[1] = -self.ball_speed[1]

        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.test_ball, self.test_ball_rect)
        self.screen.blit(self.player_up, (20, 20))
        self.screen.blit(self.player_down, (20, 50))
        self.screen.blit(self.player_left, (20, 80))
        self.screen.blit(self.player_right, (20, 110))

        for enemy_index, enemy in enumerate((self.blinky_rect, self.pinky_rect, self.inky_rect, self.clyde_rect)):
            for rect_index, rect in enumerate(enemy):
                self.screen.blit(self.enemy_sheet, (50*enemy_index+50, 30*rect_index+20), area=rect)

        self.screen.blit(self.enemy_sheet, (250, 20), area=self.scared_blue_rect)
        self.screen.blit(self.enemy_sheet, (250, 50), area=self.scared_white_rect)
        pygame.display.flip()


if __name__ == "__main__":
    frame_duration = 1/60
    game_instance = game.game()
    window_instance = Window(game_instance, size_multiplier=2)
    while 1:
        start_time = time()
        window_instance.refresh()
        game_instance.advance()
        sleep(max(0, frame_duration - (time() - start_time)))