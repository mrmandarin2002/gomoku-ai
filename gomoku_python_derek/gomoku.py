import numpy as np

test_board1 =  [[' ', ' ', ' ', 'w', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'b', 'b', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
                [' ', ' ', ' ', ' ', 'w', 'w', ' ', 'b'],
                [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' '],
                [' ', ' ', 'b', 'w', 'w', 'b', ' ', ' '],
                [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' '],
                [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' ']
                ]

class Board:

    def __init__(self, board):
        pass

    def make_move(self, move_x, move_y):
        pass

    def undo_move(self, move_x, move_y):
        pass

print(np.zeros(shape= (8,8)))