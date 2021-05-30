from ai_things import Generation
import pickle
import os


def generate_bot(desired_score, species_num):
    os.mkdir(f"species/species_{species_num}")
    print('dir made')
    current_gen = Generation()
    while max(current_gen.competitors, key = lambda x: x.gamestate.score) > desired_score:
        # current_gen.train()
        file = open(f"species/species_{species_num}/gen_{current_gen.gen_number}.pickle", "wb")
        pickle.dump(current_gen, file)
        file.close()
        current_gen = Generation(current_gen)
        

for i in range(10):
    generate_bot(1200, i)