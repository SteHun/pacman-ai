import unittest
from random import randint
import game

class GameTests(unittest.TestCase):
    def test_if_tester_works(self):
        self.assertTrue(True)
    
    def test_set_input(self):
        game_instance = game.game()
        self.assertEqual(game_instance.input, game.directions.no)
        for direction in (game.directions.up, game.directions.down, 
        game.directions.left, game.directions.right):
            game_instance.set_input(direction)
            self.assertEqual(game_instance.input, direction)

    def test_player_set_direction(self):
        game_instance = game.game()
        for direction in (game.directions.up, game.directions.down, 
        game.directions.left, game.directions.right):
            game_instance.player.set_direction(direction)
            self.assertEqual(game_instance.player.direction, direction)
        
    def test_player_set_position(self):
        game_instance = game.game()
        new_x_pos = randint(0,100)
        new_y_pos = randint(0,100)
        game_instance.player.set_position(new_x_pos, new_y_pos)
        self.assertEqual(game_instance.player.x_pos, new_x_pos)
        self.assertEqual(game_instance.player.y_pos, new_y_pos)
    
    def test_enemies_set_direction(self):
        game_instance = game.game()
        for enemy in game_instance.enemies:
            for direction in (game.directions.up, game.directions.down, 
            game.directions.left, game.directions.right):
                enemy.set_direction(direction)
                self.assertEqual(enemy.direction, direction)

    def test_enemies_set_position(self):
        game_instance = game.game()
        for enemy in game_instance.enemies:
            new_x_pos = randint(0,100)
            new_y_pos = randint(0,100)
            enemy.set_position(new_x_pos, new_y_pos)
            self.assertEqual(enemy.x_pos, new_x_pos)
            self.assertEqual(enemy.y_pos, new_y_pos)