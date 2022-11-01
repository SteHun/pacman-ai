import display
import game
from sys import exit
from time import time, sleep

import neat
import os

MAX_TIME = 10800
SCORE_WEIGHT = 5
TIME_WEIGHT_PER_SECOND = 50
LOSS_PENALTY = 5
# if __name__ == "__main__":
#     frame_duration = 1/60
#     game_instance = game.Game()
#     window_instance = display.Window(game_instance, size_multiplier=2, show_targets=True)
#     while 1:
#         start_time = time()
#         window_instance.refresh()
#         game_instance.set_input(window_instance.key_pressed)
#         game_instance.advance()
#         if game_instance.game_has_ended or game_instance.player_died:   exit(0)
#         sleep(max(0, frame_duration - (time() - start_time)))
def get_state(enemy):
    if enemy.is_eaten:  return 1
    elif enemy.is_scared:   return 2
    else:   return 0


def play_game(genome, config, show_visuals=False):
    frame_duration = 1/60
    fitness = 1000
    timer = 0
    game_instance = game.Game()
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    time_of_last_dot = 0

    if show_visuals:    window_instance = display.Window(game_instance, size_multiplier=2, show_targets=True)
    while not (game_instance.game_has_ended or game_instance.player_died):

        output = net.activate((game_instance.player.x_pos, 
                                game_instance.player.y_pos, 
                                game_instance.enemies[0].x_pos, 
                                game_instance.enemies[0].y_pos, 
                                get_state(game_instance.enemies[0]),
                                game_instance.enemies[1].x_pos, 
                                game_instance.enemies[1].y_pos, 
                                get_state(game_instance.enemies[1]),
                                game_instance.enemies[2].x_pos, 
                                game_instance.enemies[2].y_pos, 
                                get_state(game_instance.enemies[2]),
                                game_instance.enemies[3].x_pos, 
                                game_instance.enemies[3].y_pos, 
                                get_state(game_instance.enemies[3])))
        decision = output.index(max(output))
        game_instance.set_input(output.index(max(output)))

        game_instance.advance()
        timer += 1

        # fitness stuff
        if timer - (5 * 60) >= time_of_last_dot:
            time_of_last_dot = timer
            fitness -= 50

        if timer > MAX_TIME:    break

        if show_visuals:
            start_time = time()
            window_instance.refresh()
            sleep(max(0, frame_duration - (time() - start_time)))
    if show_visuals:    window_instance.close_window()
    fitness += calculate_fitness(game_instance.player.score, timer, game_instance.player.amount_of_dots, game_instance.game_has_ended)
    return fitness
    #return calculate_fitness(game_instance.player.score, timer, game_instance.player.amount_of_dots, game_instance.game_has_ended)

def calculate_fitness(score, time, dots_left, finished_level):
    if finished_level:
        return score * SCORE_WEIGHT - (time/60) * TIME_WEIGHT_PER_SECOND
    else:
        return score - dots_left

def eval_genomes(genomes, config):
    for (genome_id, genome) in genomes:
        genome.fitness = play_game(genome, config)


def train_neat(config):
    # p = neat.Checkpointer.restore_checkpoint(filename)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    winner = p.run(eval_genomes, 100)
    play_game(winner, config, show_visuals=True)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    train_neat(config)