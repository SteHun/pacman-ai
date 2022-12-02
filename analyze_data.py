# Watch out! This will get the fitness of neat checkpoints using the current fitness/game function from training.py
# Make sure it is consistent

import training
import neat
import game
import display
import os
from statistics import mean
from tqdm import tqdm

fitness_from_all_checkpoints = []

def ask_for_int(prompt, error_promt):
    while 1:
        answer = input(prompt)
        try:
            return int(answer)
        except Exception:
            print(error_promt)

def get_fitnesses_of_checkpoint(genomes, config):
    fitnesses = []
    for genome in genomes:
        fitness = training.play_game(genome[1], config)
        fitnesses.append(fitness)
        genome[1].fitness = fitness
    global fitness_from_all_checkpoints
    fitness_from_all_checkpoints.append(fitnesses)



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
    print("scanning directory...")
    filenames_in_dir = os.listdir()
    numbers_in_filenames = []
    for filename in filenames_in_dir:
        if filename.startswith("neat-checkpoint-"):
            numbers_in_filenames.append(int(filename[16:]))
    numbers_in_filenames.sort()
    print("done!")
    for i in tqdm(numbers_in_filenames, desc="determining fitness..."):
        p = neat.Checkpointer.restore_checkpoint(f"neat-checkpoint-{i}")
        p.run(get_fitnesses_of_checkpoint, 1)
    out_string = ""
    for fitnesses_of_checkpoint in fitness_from_all_checkpoints:
        for fitness in fitnesses_of_checkpoint:
            out_string += f"{fitness}, "
        out_string += "\n"
with open("fitness_results.txt", "w") as file:
    file.write(out_string)
print("done!")