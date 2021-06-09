import random
from classes import Tetris
from copy import deepcopy

num_competitors = 10
num_moves = 100
num_weights = 3


class bot:
    def __init__(self, weights):
        pass


class Competitor:
    def __init__(self, name, parent1=None, parent2=None):
        self.name = name
        self.weights = []
        self.turns_alive = 0
        # First generation
        if not parent1 and not parent2:
            self.weights = [random.uniform(0, 1) for i in range(num_weights)]
        # Proceeding generations inherit their parents characteristics randomly
        else:
            # Random cross breed
            for i in range(num_weights):
                if random.getrandbits(1):
                    self.weights.append(parent1.weights[i])
                else:
                    self.weights.append(parent2.weights[i])
        self.gamestate = Tetris()  # A new Tetris object

    def play(self):
        """
        Will play num_moves amount of moves or until death
        """
        for move in range(num_moves):
            if not self.gamestate.alive:
                print(f'Competitor {self.name} died prematurely')
                break
            best_move = self.optimal_move()
            if move%10==0:
                print(f'Turn: {move}, {best_move}')
            self.gamestate.make_move(best_move)
            self.turns_alive += 1
        print(f'Score: {self.overall_score()}\n\n')

    def overall_score(self):
        super_score = 0
        if not self.gamestate.alive:
            super_score-=1000
        return super_score+self.gamestate.score+self.turns_alive

    def calc_score(self, move):
        """
        How much does the move score based off the competitors weights?
        """
        test_board = deepcopy(self.gamestate)
        test_board.make_move(move)
        score = 0
        score -= self.weights[0] * test_board.holes #more holes worse
        score -= self.weights[1] * test_board.height_diff #more height diff worse
        score += self.weights[2] * test_board.row_score #more row_score better
        return score

    def optimal_move(self):
        """
        Returns move of form (rotation, side) optimised based off weights (calling calc_score)
        """
        best_score = float('-inf')
        best_move = None
        for rotation in range(4):
            for horizontal in range(-5,5):  # TODO: figure out horizontal range
                move = (rotation, horizontal)
                test_score = self.calc_score(move)
                if test_score > best_score:
                    best_score = test_score
                    best_move = move
        return best_move

    def mutate(self):
        for weight in self.weights:
            if not random.getrandbits(2):
                weight = random.uniform(0, 1)

    def __str__(self):
        return f"Competitor: {self.name}\nHoles: {self.weights[0]}, Height difference: {self.weights[1]}, Line clearing: {self.weights[2]}"


class Generation:
    """
    Zeroeth generation begins with randomly weighted competitors
    When a new generation is made it takes in a parent generation's children and gen number
    """

    def __init__(self, parent_gen=None):
        self.competitors = []
        self.children = []
        self.stats = {}
        # If there is a parent generation inherit the children
        if parent_gen:
            self.competitors = parent_gen.children
            self.gen_number = parent_gen.gen_number + 1
        # First generation completely random num_comp competitors
        else:
            names = iter(range(num_competitors))
            for i in range(num_competitors):
                name = next(names)
                zeros = (3-len(str(name)))*'0'
                self.competitors.append(Competitor(f'0.{zeros}{name}'))
            self.gen_number = 0
        print(f'Generation {self.gen_number} created!\n')

    def train(self):
        print('Training...\n')
        for competitor in self.competitors:
            print(competitor)
            competitor.play()
        scores = [comp.overall_score() for comp in self.competitors]
        self.stats['avg'] = sum(scores)/num_competitors
        self.stats['max'] = max(scores)
        self.stats['min'] = min(scores)
        print(f'Generation {self.gen_number} had: {self.stats}')
        self.breed()

    def breed(self):
        print('Breeding...\n\n')
        names = iter(range(num_competitors))
        # natural selection (Keep top 50%)
        viable_parents = sorted(
            self.competitors, key=lambda x: x.overall_score(), reverse=True
        )[: len(self.competitors) // 2]
        for i in range(int(num_competitors*0.85)):
            name = next(names)
            zeros = (3-len(str(name)))*'0'
            self.children.append(
                Competitor(f'{self.gen_number+1}.{zeros}{name}',random.choice(viable_parents), random.choice(viable_parents))
            )
        # mutate some of the children
        for i in range(num_competitors - int(num_competitors*0.85) ):
            name = next(names)
            zeros = (3-len(str(name)))*'0'
            child = Competitor(f'{self.gen_number+1}.{zeros}{name}',
                random.choice(viable_parents), random.choice(viable_parents)
            )
            child.mutate()
            self.children.append(child)


# Bumpiness of the board (more bumpy probably worse?? might depend on the piece)

# Number of holes created (more is worse) a hole could be an open hole would still be bad, deepness of hole

# Difference in height (greater is worse) (might be similar to height)

# Split path, next piece vs current piece