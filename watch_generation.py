# This script was used to get view how individual generations have played
# It is uncertain how effective it is and it is unstable
# It is best not to use it

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


def play_game(genome, config, show_visuals=False):
    frame_duration = 1/60
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

        if timer > MAX_TIME:    break

        if show_visuals:
            start_time = time()
            window_instance.refresh()
            sleep(max(0, frame_duration - (time() - start_time)))
    if show_visuals:    window_instance.close_window()
    print(calculate_fitness(game_instance.player.score, timer, game_instance.player.amount_of_dots, game_instance.game_has_ended))
    return calculate_fitness(game_instance.player.score, timer, game_instance.player.amount_of_dots, game_instance.game_has_ended)

def calculate_fitness(score, time, dots_left, finished_level):
    if finished_level:
        return score * SCORE_WEIGHT - (time/60) * TIME_WEIGHT_PER_SECOND
    else:
        return 500 - dots_left

def eval_genomes(genomes, config):
    global pool
    total_genomes = len(genomes)
    for i, genome in enumerate(genomes):
        print(f"{i}/ {total_genomes}")
        play_game(genome[1], config, show_visuals=True)
    for i, fitness in enumerate(fitnesses):
        genomes[i][1].fitness = fitness


def train_neat(config):
    p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-32299")
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes, 1)
    with open("winner.neat", "wb") as file:
        file.write(pickle.dumps(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    pool = Pool()
    try:
        train_neat(config)
        pool.terminate()
    except:
        pool.terminate()
        raise
