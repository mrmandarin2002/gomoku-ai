import gomoku
import gomoku2
import numpy as np
import time

test_board1 =  [[' ', ' ', ' ', 'w', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'b', 'b', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', 'w', ' ', ' '],
                [' ', ' ', ' ', ' ', 'w', 'w', ' ', 'b'],
                [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' '],
                [' ', ' ', 'b', 'w', 'w', 'b', ' ', ' '],
                [' ', ' ', ' ', ' ', 'b', ' ', ' ', ' '],
                [' ', ' ', ' ', 'b', ' ', ' ', ' ', ' ']
                ]

test_board2 =  [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'w']
                ]

board = np.array(test_board1)
board = np.where(board == " ", 0, board)
board = np.where(board == "b", 1, board)
board = np.where(board == "w", -1, board)
b = board.astype(np.int_)

row = board[5, :]
print(row)


#
#
# print(gomoku2.adjustment(b, 4, 6))
# print(gomoku2.detect_row(board, 1, 3, 7, 3, 1, -1))

# print(gomoku2.move(test_board1, 'w'))

'''
Testing move function 
'''
# a = time.time()
# print(gomoku.move(test_board1, 'b'))
# b = time.time()
# print(b-a)
#
# c = time.time()
# print(gomoku2.move(test_board1, 'b'))
# d = time.time()
# print(d-c)




# t0 = time.time()
#
# def get_free_squares_adj(board):
#     free_spaces = set()
#     for i in range(0, 8):
#         for e in range(0, 8):
#             #don't waste time (maybe?)
#             if board[i, e] == " ":
#                 pass
#
#             #all the ifs now
#             else:
#                 for b in range(i-1, i+2):
#                     for c in range(e-1, e + 2):
#                         try:
#                             if board[b, c] == " ":
#                                 free_spaces.add((b, c))
#                         except:
#                             pass
#
#     free = np.array(list(free_spaces))
#     return free
#
# board = np.array(test_board2)
#
# t = time.time()
# print(t-t0)
#
# # print(get_free_squares_adj(board))
#
# # board = np.array(test_board1)
#
# # t0 = time.time()
# board = np.where(board == " ", 0, board)
# board = np.where(board == "b", 1, board)
# board = np.where(board == "w", -1, board)
# board = board.astype(np.int_)
# # t = time.time()

'''
board2 = np.array(test_board1)

t1 = time.time()
board2[board2 == " "] = 0
board2[board2 == "b"] = 1
board2[board2 == "w"] = 2
board2 = board2.astype(np.int_)
t2 = time.time()
print(t2-t1)
'''

#
# # print(board)
#
# row = board2[1]
# print(row)
# print(np.transpose(np.nonzero(row)))

# a = np.array([1, 2, 3, 4, 5, 6, 7, 8])
# print(np.all(a == [1, 2, 3, 4, 5]))