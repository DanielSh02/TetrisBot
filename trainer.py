from ai_things import Generation
import pickle
import glob

def generate_bot(desired_score):
    species_num = len(glob.glob("species/*"))
    current_gen = Generation()
    #while score is still less than desired score
    while max([comp.gamestate.score for comp in current_gen.competitors]) < desired_score:
        #train the generation
        current_gen.train()
        #update current gen to be the kids
        current_gen = Generation(current_gen)
    print('Success')
    file = open(f"species/species_{species_num}.pickle", "wb")
    pickle.dump(current_gen, file)
    file.close()


for i in range(10):
    generate_bot(10000)