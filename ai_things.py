import random
from classes import Tetris
from copy import deepcopy

num_moves = 100
num_weights = 4

class bot:
    def __init__(self, weights):
        pass


class Competitor:
    def __init__(self, parent1=None, parent2=None):
        self.weights = []
        #First generation
        if not parent1 and not parent2:
            self.weights = [random.uniform(0, 1) for i in range(num_weights)]
        #Proceeding generations inherit their parents characteristics randomly
        else:
            #Random cross breed
            for i in range(num_weights):
                if random.getrandbits(1):
                    self.weights[i] = parent1.weights[i]
                else:
                    self.weights[i] = parent2.weights[i]
        self.gamestate = Tetris() # A new Tetris object

    def play(self):
        """
        Will play num_moves amount of moves or until death
        """
        for move in range(num_moves):
            self.gamestate.make_move(self.optimal_move())

    def calc_score(self, move):
        """
        How much does the move score based off the competitors weights?
        """
        score = 0
        test_board = deepcopy(self.gamestate)

    def optimal_move(self):
        """
        Returns move of form (switch, rotation, side) optimised based off weights (calling calc_score)
        """
        best_score = -1
        best_move = None
        for switch in range(2):
            for rotation in range(4):
                for horizontal in range(100): #TODO: figure out horizontal range
                    move = (switch, rotation, horizontal)
                    test_score = self.calc_score(move)
                    if test_score>best_score:
                        best_score = test_score
                        best_move = move
        return best_move

    

    def __str__(self):
        return f'Weights - Holes: {self.weights[0]}, Bumpiness: {self.weights[1]}, Height difference: {self.weights[2]}, Line clearing: {self.weights[3]}'


class Generation():
    """
    Zeroeth generation begins with randomly weighted competitors
    When a new generation is made it takes in a parent generation's children and gen number
    """
    def __init__(self, parent_gen=None):
        self.competitors = []
        self.children = []

        # If there is a parent generation inherit the children
        if parent_gen:
            self.competitors = parent_gen.children
            self.gen_number = parent_gen.gen_number+1
        #First generation completely random 100 competitors
        else:
            self.competitors = [Competitor() for i in range(100)]
            self.gen_number = 0

    def train(self):
        for competitor in self.competitors:
            competitor.play()
        self.breed()

    def breed(self):
        #natural selection (Keep top 50%)
        viable_parents = sorted(self.competitors, key = lambda x: x.gamestate.score, reverse = True)[:len(self.competitors)//2]
        for i in range(100):
            self.children.append(Competitor(random.choice(viable_parents), random.choice(viable_parents)))


#Bumpiness of the board (more bumpy probably worse?? might depend on the piece) negative weight

#Number of holes created (more is worse) negative weight, a hole could be an open hole would still be bad, deepness of hole

#Difference in height (greater is worse) negative weight (might be similar to height)

#Split path, next piece vs current piece