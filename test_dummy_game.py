import unittest
from random import randint
import game

class GameTests(unittest.TestCase):
    def test_if_tester_works(self):
        self.assertTrue(True)
    
    def test_set_input(self):
        game_instance = game.Game()
        self.assertEqual(game_instance.input, game.directions.no)
        for direction in (game.directions.up, game.directions.down, 
        game.directions.left, game.directions.right):
            game_instance.set_input(direction)
            self.assertEqual(game_instance.input, direction)

    def test_player_set_direction(self):
        game_instance = game.Game()
        for direction in (game.directions.up, game.directions.down, 
        game.directions.left, game.directions.right):
            game_instance.player.set_direction(direction)
            self.assertEqual(game_instance.player.direction, direction)
        
    def test_player_set_position(self):
        game_instance = game.Game()
        new_x_pos = randint(0,100)
        new_y_pos = randint(0,100)
        game_instance.player.set_position(new_x_pos, new_y_pos)
        self.assertEqual(game_instance.player.x_pos, new_x_pos)
        self.assertEqual(game_instance.player.y_pos, new_y_pos)
    
    def test_enemies_set_direction(self):
        game_instance = game.Game()
        for enemy in game_instance.enemies:
            for direction in (game.directions.up, game.directions.down, 
            game.directions.left, game.directions.right):
                enemy.set_direction(direction)
                self.assertEqual(enemy.direction, direction)

    def test_enemies_set_position(self):
        game_instance = game.Game()
        for enemy in game_instance.enemies:
            new_x_pos = randint(0,100)
            new_y_pos = randint(0,100)
            enemy.set_position(new_x_pos, new_y_pos)
            self.assertEqual(enemy.x_pos, new_x_pos)
            self.assertEqual(enemy.y_pos, new_y_pos)
    
    def test_player_is_moving(self):
        game_instance = game.Game()
        for _ in range(300):
            old_x_pos, old_y_pos = game_instance.player.x_pos, game_instance.player.y_pos
            game_instance.advance()
            self.assertNotEqual(old_x_pos, game_instance.player.x_pos)
            self.assertNotEqual(old_y_pos, game_instance.player.y_pos)

    def test_player_stays_in_bounds(self):
        game_instance = game.Game()
        for _ in range(300):
            game_instance.advance()
            self.assertLessEqual(game_instance.player.x_pos, game_instance.player.max_x_pos)
            self.assertLessEqual(game_instance.player.y_pos, game_instance.player.max_y_pos)
            self.assertGreaterEqual(game_instance.player.x_pos, game_instance.player.min_x_pos)
            self.assertGreaterEqual(game_instance.player.y_pos, game_instance.player.min_y_pos)
    
    def test_enemies_are_moving(self):
        game_instance = game.Game()
        old_positions = [None for _ in range(4)]
        for _ in range(300):
            for i, enemy in enumerate(game_instance.enemies):
                old_positions[i]=  game_instance.player.x_pos, game_instance.player.y_pos
            game_instance.advance()
            for i, enemy in enumerate(game_instance.enemies):
                self.assertNotEqual(old_positions[i][0], game_instance.enemies[i].x_pos)
                self.assertNotEqual(old_positions[i][1], game_instance.enemies[i].y_pos)
    
    def test_enemies_stay_in_bounds(self):
        game_instance = game.Game()
        for _ in range(300):
            game_instance.advance()
            for enemy in game_instance.enemies:
                self.assertLessEqual(enemy.x_pos, enemy.max_x_pos)
                self.assertLessEqual(enemy.y_pos, enemy.max_y_pos)
                self.assertGreaterEqual(enemy.x_pos, enemy.min_x_pos)
                self.assertGreaterEqual(enemy.y_pos, enemy.min_y_pos)
    