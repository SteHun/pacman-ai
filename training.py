# All files are currently set up to play the run with the player spawning normally
# To switch to random spawning, replace 'import game' with 'import game_random_spawn as game' in the following files
#   training.py
#   display.py
#   play.py
# This could also be done with the 'analyze_data.py' and the 'watch_generation.py' files, but those are unstable, unnecessary and difficul to use
# 
# To switch to the version where fitness starts at 256, uncomment line 73 of this file

import display
import game
from sys import exit
from time import time, sleep
from multiprocessing import Pool
import pickle

import neat
import os

MAX_TIME = 10800
SCORE_WEIGHT = 5
TIME_WEIGHT_PER_SECOND = 50
def get_state(enemy):
    if enemy.is_eaten:  return 1
    elif enemy.is_scared:   return 2
    else:   return 0

# this function is run for every neural network
def play_game(genome, config, show_visuals=False):
    frame_duration = 1/60
    timer = 0
    game_instance = game.Game()
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    time_of_last_dot = 0

    if show_visuals:    window_instance = display.Window(game_instance, size_multiplier=2, show_targets=True)
    # runs the game while it is not over
    while not (game_instance.game_has_ended or game_instance.player_died):
        # get the results from the network
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
        # if the player takes too long, stop the game
        if timer > MAX_TIME:    break

        if show_visuals:
            start_time = time()
            window_instance.refresh()
            sleep(max(0, frame_duration - (time() - start_time)))
    if show_visuals:    window_instance.close_window()
    return calculate_fitness(game_instance.player.score, timer, game_instance.player.amount_of_dots, game_instance.game_has_ended)
# this is the fitness function
def calculate_fitness(score, time, dots_left, finished_level):
    if finished_level:
        return 500
    else:
        # return 500 - dots_left
        return 244 - dots_left
# this function runs the game for every net in a generation
def eval_genomes(genomes, config):
    global pool
    global generation_number
    fitnesses = pool.starmap(play_game, [(genome[1], config) for genome in genomes])
    for i, fitness in enumerate(fitnesses):
        genomes[i][1].fitness = fitness
    if (generation_number + 1) % 100 == 0:
        append_list_to_file("fitness_results.txt", fitnesses)
    generation_number += 1
# this is to document the results
def append_list_to_file(filename, list_to_append):
    out_string = ""
    for i in list_to_append:
        out_string += f"{i},"
    out_string += "\n"
    with open(filename, "a") as file:
        file.write(out_string)
# this initializes the training
def train_neat(config):
    # p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-46599")
    p = neat.Population(config)
    # p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))
    with open("fitness_results.txt", "x") as file:
        pass
    winner = p.run(eval_genomes, 500)
    # play_game(winner, config, show_visuals=True)
    with open("winner.neat", "wb") as file:
        file.write(pickle.dumps(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    pool = Pool(12)
    generation_number = 0
    try:
        train_neat(config)
        pool.terminate()
    except:
        pool.terminate()
        raise
