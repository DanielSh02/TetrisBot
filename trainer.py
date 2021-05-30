from ai_things import Generation
import pickle


def generate_bot(desired_score):
    current_gen = Generation()
    while max(current_gen.competitors, key = lambda x: x.gamestate.score) > desired_score:
        current_gen.train()
        current_gen = Generation(current_gen)
