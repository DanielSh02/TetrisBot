from copy import deepcopy
import random
import numpy as np

piece_types = ['J', 'L', 'I', 'T', 'S', 'Z', 'O']
piece_layouts = dict(J=np.array([[0, 1, 1],
                                 [0, 0, 1],
                                 [0, 0, 1]]),
                     L=np.array([[0, 0, 1],
                                 [0, 0, 1],
                                 [0, 1, 1]]),
                     I=np.array([[0, 0, 1, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 1, 0],
                                 [0, 0, 1, 0]]),
                     T=np.array([[0, 0, 1],
                                 [0, 1, 1],
                                 [0, 0, 1]]),
                     S=np.array([[0, 1, 0],
                                 [0, 1, 1],
                                 [0, 0, 1]]),
                     Z=np.array([[0, 0, 1],
                                 [0, 1, 1],
                                 [0, 1, 0]]),
                     O=np.array([[1, 1],
                                 [1, 1]]))

piece_colors = dict(
    J=(0, 0, 255),
    L=(255, 127, 0),
    I=(0, 255, 255),
    T=(128, 0, 128),
    S=(0, 255, 0),
    Z=(255, 0, 0),
    O=(255, 255, 0)
)


class Tetris:
    def __init__(self):
        self.board = [[None] * 24 for i in range(10)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.level = 0
        self.frames = 0
        # print('Current Piece' + str(self.current_piece))
        # print('Next piece' + str(self.next_piece))

    def down(self):
        if self.collides(self.current_piece, [0, -1]):
            print('Freeze!')
            self.freeze()
        else:
            self.current_piece.move([0, -1])

    def side(self, direction):
        test_piece = deepcopy(self.current_piece)
        test_piece.move(direction)
        if not self.collides(test_piece):
            self.current_piece.move(direction)

    def rotate_clockwise(self):
        test_piece = deepcopy(self.current_piece)
        test_piece.rotate_clockwise()
        if not self.collides(test_piece):
            self.current_piece.rotate_clockwise()
        else:
            test_moves = [[1, 0], [-1, 0], [0, 1], [1, 1], [-1, -1], [1, -1], [-1, 1]]
            for move in test_moves:
                if not self.collides(test_piece, move):
                    print('valid')
                    self.current_piece.move(move)
                    self.current_piece.rotate_clockwise()
                    break
        print('rotation end')


    def drop(self):
        test_piece = deepcopy(self.current_piece)
        distance = 0
        for i in range(24):
            if self.collides(test_piece, [0, -1]):
                distance = i
                break
            test_piece.move([0, -1])
        self.current_piece.move([0, -distance])
        self.freeze()

    def freeze(self):
        for square in self.current_piece.squares:
            self.board[square[0]][square[1]] = self.current_piece.color
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.clear_rows()

    def collides(self, piece, move=[0, 0]):
        test_piece = deepcopy(piece)
        test_piece.move(move)
        for coord in test_piece.squares:
            if coord[1] < 0 or coord[0] < 0 or coord[0] >= 10:
                return True
            if self.board[coord[0]][coord[1]] is not None:
                return True
        return False

    def clear_rows(self):
        full_rows = []
        for i in range(24):
            counter = 0
            for j in range(10):
                if self.board[j][i] is not None:
                    counter += 1
            if counter == 10:
                full_rows.append(i)
        counter = 0
        self.score += self.scoring(len(full_rows))
        for i in full_rows:
            for column in self.board:
                column.pop(i - counter)
                column.append(None)
            counter += 1
        print(self.score)

    def new_piece(self):
        piece_type = random.choice(piece_types)
        piece = Piece(piece_type, 4, 20)
        return piece

    def restart(self):
        self.board = [[None] * 24 for i in range(10)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()

    def scoring(self, rows_cleared):
        # TODO: Make scoring count the amount the piece has been dropped
        if rows_cleared == 1:
            return 40 * (self.level + 1)
        if rows_cleared == 2:
            return 100 * (self.level + 1)
        if rows_cleared == 3:
            return 300 * (self.level + 1)
        if rows_cleared == 4:
            return 1200 * (self.level + 1)
        else:
            return 0

class Piece:
    def __init__(self, type, column, row):
        self.x = column
        self.y = row
        self.type = type
        self.color = piece_colors[type]
        self.rotation = 0
        self.layout = piece_layouts[type]
        self.squares = []
        self.generate_squares()

    def generate_squares(self):
        self.squares = []
        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                if self.layout[i][j] != 0:
                    x = i + self.x
                    y = j + self.y
                    self.squares.append([x, y])

    def move(self, vector):
        self.x += vector[0]
        self.y += vector[1]
        self.generate_squares()

    def rotate_clockwise(self):
        self.layout = np.rot90(self.layout, 3, axes=(0, 1))
        self.generate_squares()
