from copy import deepcopy
import random
import numpy as np

piece_types = ['J', 'L', 'I', 'T', 'S', 'Z', 'O']
piece_layouts = dict(
    J=np.array([[0, 0, 0], [1, 0, 0], [1, 1, 1]]),
    L=np.array([[0, 0, 0], [0, 0, 1], [1, 1, 1]]),
    I=np.array([[1, 1, 1, 1]]),
    T=np.array([[0, 0, 0], [0, 1, 0], [1, 1, 1]]),
    S=np.array([[0, 0, 0], [1, 1, 0], [0, 1, 1]]),
    Z=np.array([[0, 0, 0], [0, 1, 1], [1, 1, 0]]),
    O=np.array([[1, 1], [1, 1]])
)

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
        # print('Current Piece' + str(self.current_piece))
        # print('Next piece' + str(self.next_piece))

    def down(self):
        test_piece = deepcopy(self.current_piece)
        test_piece.move([0, -1])
        if self.collides(test_piece):
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
        test_piece.layout = np.rot90(test_piece.layout, 3, axes=(0, 1))
        test_piece.generate_squares()
        if not self.collides(test_piece):
            self.current_piece.rotate_clockwise()
        else:
            test_piece.move([1, 0])
            if not self.collides(test_piece):
                self.current_piece.rotate_clockwise()
                self.current_piece.move([1, 0])
            else:
                test_piece.move([-2, 0])
                if not self.collides(test_piece):
                    self.current_piece.rotate_clockwise()
                    self.current_piece.move([-1, 0])

    def drop(self):
        test_piece = deepcopy(self.current_piece)
        distance = 0
        for i in range(24):
            if self.collides(test_piece):
                distance = i - 1
                # print('collided!')
                break
            test_piece.move([0, -1])
            print(test_piece.squares)
        # print(distance)
        self.current_piece.move([0, -distance])
        print(self.current_piece.squares)
        self.freeze()

    def freeze(self):
        for square in self.current_piece.squares:
            self.board[square[0]][square[1]] = self.current_piece.color
            # TODO: Make board[i][j] show the color of the square
        self.current_piece = self.next_piece
        self.next_piece = self.new_piece()
        self.clear_rows()
        # print(self.board)

    def collides(self, piece):
        for coord in piece.squares:
            # print(coord)
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
                full_rows.append(j)
        counter = 0
        for i in range(len(full_rows)):
            for column in self.board:
                column.pop(i - counter)
                column.append(None)

    def new_piece(self):
        piece_type = random.choice(piece_types)
        piece = Piece(piece_type, 4, 20)
        return piece


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
        self.generate_squares