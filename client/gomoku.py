from socket import *
import multiprocessing, timeit
import numpy as np
import random

#Derek's Stuff ---------------------

ROWS = 8
COLS = 8
zobrist_table = [[[0,0] for x in range(COLS)] for y in range(ROWS)]
sur_squares = [[[] for y in range(COLS)] for x in range(ROWS)]
num_to_square = [[0,0] for x in range(64)]
threat_weight = [[0] * 128 for x in range(7)]
threat_patterns = [[] for x in range(7)]


HOST = "192.168.100.109"
PORT = 5050
BUFFER_SZ = 128
WELCOME_MESSAGE = "Meow"
DISCONNECT_MESSAGE = "Woof"

nodes_visited = [0]

server_move_x, server_move_y = 0, 0

def in_board(x, y):
    if x >= 0 and x < ROWS and y >= 0 and y < COLS:
        return True
    return False

def add_pattern(pat, pattern_weight):
    pat_hash = 0
    for x in range(len(pat)):
        pat_hash = pat_hash << 1
        if pat[x] == 'X':
            pat_hash += 1
    threat_weight[len(pat)][pat_hash] = pattern_weight
    threat_patterns[len(pat)].append(pat_hash)
    
def fill_patterns():
    add_pattern("XXXXX", 1000000)
    add_pattern(".XXXX.", 10000)
    add_pattern("XXXX.", 900)
    add_pattern("XXX.X", 1000)
    add_pattern("XX.XX", 1250)
    add_pattern("X.XXX", 1000)
    add_pattern(".XXXX", 900)

    add_pattern(".XXX.", 400)
	#add_pattern(".XXX", 300)
	#add_pattern("XXX.", 300)
    add_pattern(".XX.X.", 700)
    add_pattern(".X.XX.", 700)
    print(threat_patterns)

def preprocessing():
    SQ_RADIUS = 1
    fill_patterns()
    # fill surrounding squares table
    for x in range(0, ROWS):
        for y in range(0, COLS):
            for cor_x in range(-SQ_RADIUS, SQ_RADIUS + 1):
                for cor_y in range(-SQ_RADIUS, SQ_RADIUS + 1):
                    cur_x = x + cor_x
                    cur_y = y + cor_y
                    if in_board(cur_x, cur_y) and not(cur_x == x and cur_y == y):
                        sur_squares[x][y].append(cur_x * ROWS + cur_y)
                        num_to_square[cur_x * ROWS + cur_y] = (cur_x, cur_y)


    # fill zobrist table
    for i in range(0, ROWS):
        for j in range(0, COLS):
            for k in range(0, 2):
                zobrist_table[i][j][k] = random.randint(1000, 10000000000000)


class server:

    #removes unecessary shit from board so server has an easier time processing this shit
    def clean_board(self, board):
        board_str = ""
        for letter in str(board):
            if letter != '[' and letter != ']' and letter != ',' and letter != ',' and letter != "'":
                board_str += letter
        print("BOARD: \n:", board_str)
        return board_str

    #send board to server and the coordinates of the move will be returned
    def send_board(self, board):
        self.s.send(self.clean_board(board).encode())
        moves = self.s.recv(BUFFER_SZ).decode()
        print("RETURNED MESSAGE:", moves)

    def __del__(self):
        self.s.send(DISCONNECT_MESSAGE.encode())
        print("Ciao")

    def __init__(self):
        print("Initalizing connection with server")
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((HOST, PORT))
        print("Done Initializing")
        welcome_message = self.s.recv(BUFFER_SZ).decode()
        if welcome_message:
            print("Connection with server successful!")
        else:
            print("Something is wrong with the connection :(")

class b:

    def get_score_in_line(self, cor_x, cor_y, move_x, move_y, p_length, diagonal):
        white_overlay = 0
        black_overlay = 0
        start_x = 0
        start_y = 0
        cur_x = 0
        cur_y = 0
        if not diagonal:
            start_x = max(0, cor_x - (move_x * (p_length - 1)))
            start_y = max(0, cor_y - (move_y * (p_length - 1)))
        else:
            start_x  = cor_x - (move_x * (p_length - 1))
            start_y  = cor_y - (move_y * (p_length - 1))
            while not in_board(start_x, start_y):
                start_x += move_x
                start_y += move_y
        black_pieces = 0
        white_pieces = 0
        cur_score = 0
        cur_x = start_x
        cur_y = start_y
        for i in range(p_length):
            if not in_board(cur_x, cur_y):
                return 0
            black_overlay = black_overlay << 1
            white_overlay = white_overlay << 1
            #print(cur_x, cur_y)
            if self.board[cur_x][cur_y] == 'b':
                black_overlay += 1
                black_pieces += 1
            elif self.board[cur_x][cur_y] == 'w':
                white_overlay += 1
                white_pieces += 1
            cur_x += move_x
            cur_y += move_y

        for i in range(p_length):

            #fucking beautiful jesus
            if not black_pieces:
                cur_score -= threat_weight[p_length][white_overlay]
            elif not white_pieces:
                cur_score += threat_weight[p_length][black_overlay]
            
            if i != p_length - 1:
                if abs(cor_x - cur_x) >= p_length or abs(cor_y - cur_y) >= p_length or not in_board(cur_x, cur_y):
                    break
                if self.board[start_x][start_y] == 'b':
                    black_overlay -= (1 << (p_length - 1))
                    black_pieces -= 1
                elif self.board[start_x][start_y] == 'w':
                    white_overlay -= (1 << (p_length - 1))
                    white_pieces -= 1
            
            black_overlay = black_overlay << 1
            white_overlay = white_overlay << 1
            if self.board[cur_x][cur_y] == 'b':
                black_overlay += 1
                black_pieces += 1
            elif self.board[cur_x][cur_y] == 'w':
                white_overlay += 1
                white_pieces += 1

            start_x += move_x
            start_y += move_y
            cur_x += move_x
            cur_y += move_y

        return cur_score

    def get_cor_score(self, cor_x, cor_y):
        cur_score = 0
        for x in range(5, 7):
            cur_score += self.get_score_in_line(cor_x, cor_y, 0, 1, x, False)
            cur_score += self.get_score_in_line(cor_x, cor_y, 1, 0, x, False)
            cur_score += self.get_score_in_line(cor_x, cor_y, 1, 1, x, True)
            cur_score += self.get_score_in_line(cor_x, cor_y, 1, -1, x, True)
        return cur_score

    def score_change(self, move_x, move_y, undo):
        piece = 'b'
        if not self.cur_color:
            piece = 'w'
        before_score = self.get_cor_score(move_x, move_y)
        if not undo:
            self.board[move_x][move_y] = piece
        else:
            self.board[move_x][move_y] = ' '
        after_score = self.get_cor_score(move_x, move_y)
        if not undo:
            self.board[move_x][move_y] = ' '
        else:
            self.board[move_x][move_y] = piece
        self.board_score += (after_score - before_score)

    def make_move(self, move_x, move_y):
        self.score_change(move_x, move_y, False)
        if self.cur_color:
            self.board[move_x][move_y] = 'b'
        else:
            self.board[move_x][move_y] = 'w'

        self.hash_val = self.hash_val ^ zobrist_table[move_x][move_y][self.cur_color]
        for move in sur_squares[move_x][move_y]:
            square_x, square_y = num_to_square[move]
            self.visited[move] += 1
            if self.board[square_x][square_y] == ' ':
                self.move_list.add(move)
       
        self.cur_color = not self.cur_color

    def undo_move(self, move_x, move_y):
        self.score_change(move_x, move_y, True)
        square = move_x * ROWS + move_y
        self.board[move_x][move_y] = ' '
        self.hash_val = self.hash_val ^ zobrist_table[move_x][move_y][not self.cur_color]
        
        for move in sur_squares[move_x][move_y]:
            self.visited[move] -= 1
            if not self.visited[move]:
                self.move_list.remove(move)
        
        if self.visited[square]:
            self.move_list.add(square)
        
        self.cur_color = not self.cur_color

    def mini_max(self, depth, alpha, beta):
        if depth == 0 or abs(self.board_score > 50000):
            return self.board_score

        if self.hash_val in self.t_table:
            return self.t_table[self.hash_val]

        maximize = -1e9
        best_move = 0

        m_list = list(self.move_list)
        #black
        if self.cur_color:
            for move in m_list:
                move_x = int(move / ROWS)
                move_y = move % COLS
                self.make_move(move_x, move_y)
                score = self.mini_max(depth - 1, alpha, beta)
                self.score_table[move_x][move_y] = score
                if score > maximize:
                    maximize = score
                    best_move = move
                alpha = max(alpha, maximize)
                self.undo_move(move_x, move_y)

                if beta <= alpha:
                    break

        else:
            maximize = 1e9
            for move in m_list:
                move_x = int(move / ROWS)
                move_y = move % COLS
                self.make_move(move_x, move_y)
                score = self.mini_max(depth - 1, alpha, beta)
                self.score_table[move_x][move_y] = score
                if score < maximize:
                    maximize = score
                    best_move = move
                alpha = min(alpha, maximize)
                self.undo_move(move_x, move_y)
                if beta <= alpha:
                    break

        self.t_table[self.hash_val] = maximize
        return maximize


    def __init__(self, board, col):
        self.score_table = [[0 for y in range(COLS)] for x in range(ROWS)]
        self.t_table = {}
        self.max_depth = 3
        self.board_score = 0
        self.move_list = set()
        self.visited = [0 for y in range(COLS * ROWS)]
        self.hash_val = 0
        self.board = board
        for x in range(ROWS):
            for y in range(COLS):
                if self.board[x][y] == 'b':
                    self.cur_color = True
                    self.make_move(x, y)
                elif self.board[x][y] == 'w':
                    self.cur_color = False
                    self.make_move(x,y)
        self.cur_color = (col == 'b')
        #self.print_board()

    def print_board(self):
        print("BOARD SCORE:", self.board_score)
        print("    ", end = '')
        for x in range(ROWS):
            print(str(x) + '    ', end = '')
        print('\n', end = '')
        for num, row in enumerate(self.board):
            print(num, row)
        #print('\n')
        #print(self.visited)
        #print('\n')
        print(len([num_to_square[move] for move in sorted(self.move_list)]))
        print('\n')
        print("HASH VALUE:", self.hash_val)

#initalizes server as the file is imported
#server_connection = server()      

test_board1 =  [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', 'w', ' '],
                [' ', ' ', ' ', ' ', 'b', 'b', ' ', ' '],
                [' ', 'b', 'w', 'w', 'b', ' ', ' ', ' '],
                [' ', ' ', ' ', 'b', ' ', 'w', ' ', ' '],
                [' ', ' ', ' ', ' ', 'w', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                ]

test_board2 =  [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', 'w', 'w', ' ', ' ', ' '],
                [' ', ' ', ' ', 'b', 'b', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                ]

#note that col refers to colour
def move(board, col):

    test_board = b(board, col)
    '''
    try:
        global server_connection
        server_connection.send_board(board)
    except Exception as e:
        print("ERROR: ", e)
    '''

preprocessing()
#move(test_board2, 'b')

start_time = timeit.default_timer()

bb = b(test_board1, 'b')
print(bb.mini_max(3, -1e9, 1e9))
bb.print_board()
for row in bb.score_table:
    print(row)
'''
bb.print_board()
bb.make_move(3,2)
bb.print_board()
bb.make_move(3,0)
bb.print_board()
bb.make_move(3,3)
bb.print_board()
bb.undo_move(3,3)
bb.print_board()
bb.undo_move(3,0)
bb.print_board()
bb.undo_move(3,2)
bb.print_board()

for x in range(5000):
    bb.make_move(1,1)
    bb.undo_move(1,1)
'''


print("TIME:", timeit.default_timer() - start_time)






    
    




