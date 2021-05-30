from numpy import exp
import doctest
import random
from classes import Tetris

num_moves = 100
num_weights = 3

class Competitor:
    def __init__(self, parent1=None, parent2=None):
        self.weights = []
        #First generation
        if not parent1 and not parent2:
            self.weights = [random.getrandbits(1) for i in range(num_weights)]
        #Proceeding generations inherit their parents characteristics randomly
        else:
            #Random cross breed
            for i in range(num_weights):
                if random.getrandbits(1):
                    self.weights[i] = parent1.weights[i]
                else:
                    self.weights[i] = parent2.weights[i]
        self.gamestate = Tetris() # A new Tetris object

    def optimal_move(self):
        best_fit = -1
        best_move = None

    def calc_score(self, move):
        score = 0
        test_board = 

    def __str__(self):
        return f'Weights - Holes: {self.weights[0]}, Bumpiness: {self.weights[1]}, Height difference: {self.weights[2]}'

class Generation():
    """
    Zeroeth generation begins with randomly weighted competitors
    At the end of a run (each competitor 100 moves max) competitors cross breed and create a new generation
    """
    def __init__(self, parent_gen=None):
        self.competitors = []
        if parent_gen:
            self.competitors = parent_gen
        self.ancestors = [Competitor() for i in range(100)]
        self.children = None
        self.gen = parent_gen
    def natural_selection(self):
        """
        Takes the top half of competitors
        >>> natural_selection([(0,[]),(900,[]),(12000,[]),(800,[])]
        
        """
        
        return self.children.sorted(key = lambda x: x.gamestate.score)[-len(self.children)//2:]
    def cross_breed():


#Bumpiness of the board (more bumpy probably worse?? might depend on the piece) negative weight

#Number of holes created (more is worse) negative weight

#Difference in height (greater is worse) negative weight (might be similar to height)

#Split path, next piece vs current piece

"""
Best moves:


"""




def sigmoid(x):
    """
    >>> int(sigmoid(0.458)*10000)
    6125
    """
    return 1 / (1 + exp(-x))



if __name__ == "__main__":
    doctest.testmod()

