import numpy as np
from operator import itemgetter

'''
still need to implement:
    alpha beta 
    using numpy -> faster board query???
                -> boolean masking (?)
    transposition tables 
'''

def move(board, col):
    if col == "b":
        col = 1
        opp = -1
    else:
        col = -1
        opp = 1

    board = np.array(board)
    board = np.where(board == " ", 0, board)
    board = np.where(board == "b", 1, board)
    board = np.where(board == "w", -1, board)

    b = board.astype(np.int_)

    moves = get_free_squares_adj(b)

    if len(moves) == 0:
        return (4, 4)

    else:
        best_move = (-1, -1)
        if col == 1:
            best_val = -100000
            for move in moves:
                b[move[0], move[1]] = col
                value = minimax(b, 1, opp, -1000000, 1000000)

                if value > best_val:
                    best_move = move
                    best_val = value

                b[move[0], move[1]] = 0

        else:
            best_val = 100000
            for move in moves:
                b[move[0], move[1]] = col

                value = minimax(b, 1, opp, -1000000, 1000000)

                if value < best_val:
                    best_move = move
                    best_val = value

                b[move[0], move[1]] = 0

    best_move = (best_move[0], best_move[1])

    return best_move


def minimax(board, depth, col, alpha, beta):
    # black wants to maximize while white will want to minimize

    free_squares = get_free_squares_adj(board)
    cur = analyze(board)

    if cur == 100000 or cur == -100000:
        return cur

    if len(free_squares) == 0:
        return 0

    if depth == 0:
        return cur

    if col == 1:
        best = -1000000
        for move in free_squares:
            board[move[0], move[1]] = 1
            value = minimax(board, depth - 1, -1, alpha, beta)
            best = max(best, value)
            alpha = max(alpha, best)
            board[move[0], move[1]] = 0
            if beta <= alpha:
                break
        return best

    else:
        best = 1000000
        for move in free_squares:
            board[move[0], move[1]] = -1
            value = minimax(board, depth - 1, 1, alpha, beta)
            best = min(best, value)
            beta = min(beta, best)
            board[move[0], move[1]] = 0
            if beta <= alpha:
                break
        return best


def get_free_squares_adj(board):
    '''
    want to make faster
    check if surrounding element in set?
    don't want to check middle again
    '''

    free_spaces = set()
    for i in range(0, 8):
        for e in range(0, 8):
            #don't waste time (maybe?)
            if board[i, e] == 0:
                pass

            #all the ifs now
            else:
                for b in range(i-1, i+2):
                    for c in range(e-1, e + 2):
                        try:
                            if board[b, c] == 0:
                                free_spaces.add((b, c))
                        except:
                            pass

    free = np.array(list(free_spaces))

    return free

def adjustment(board, x, y):
    #New Score
    row = board[y, :]

    col = board[:, x]

    left_diag = []
    a, b = y, x
    while a != 0 and b != 0:
        a -= 1
        b -= 1
    while a != 8 and b != 8:
        left_diag.append(board[a, b])
        a += 1
        b += 1
    np.array(left_diag)

    right_diag = []
    c, d = y, x
    while c != 7 and d != 0:
        c += 1
        d -= 1
    while c != -1 and d != 8:
        right_diag.append(board[c, d])
        c -= 1
        d += 1

    np.array(right_diag)

    #Old score
    board[y, x] = 0
    row2 = board[y, :]


    col2 = board[:, x]


    left_diag2 = []
    a, b = y, x
    while a != 0 and b != 0:
        a -= 1
        b -= 1
    while a != 8 and b != 8:
        left_diag2.append(board[a, b])
        a += 1
        b += 1
    np.array(left_diag2)


    right_diag2 = []
    c, d = y, x
    while c != 7 and d != 0:
        c += 1
        d -= 1
    while c != -1 and d != 8:
        right_diag2.append(board[c, d])
        c -= 1
        d += 1

    np.array(right_diag2)

    L = [row, col, left_diag, right_diag]
    L2 = [row2, col2, left_diag2, right_diag2]

    if analyze(L) == 100000 or analyze(L) == -100000:
        return analyze(L)

    return analyze(L) - analyze(L2)

def analyze(L):
    b_5, w_5 = 0, 0

    open_b_4, open_w_4 = 0, 0
    open_b_3, open_w_3 = 0, 0

    semiopen_b_4, semiopen_w_4 = 0, 0
    semiopen_b_3, semiopen_w_3 = 0, 0

    open_b_2, open_w_2 = 0, 0
    semiopen_b_2, semiopen_w_2 = 0, 0

    for a in L:
        '''hahahahahhaahahahelpahahahahahhahahha'''

    return (-2000 * open_w_4 +
            -800 * semiopen_w_4 +
            -300 * open_w_3 +
            -10 * semiopen_w_3 +
            -5 * open_w_2 +
            semiopen_w_2 +

            2000 * open_b_4 +
            800 * semiopen_b_4 +
            300 * open_b_3 +
            10 * semiopen_b_3 +
            5 * open_b_2 +
            semiopen_b_2)

def analyze_row(board, y):
    '''still need to look for bbb b patterns'''
    '''loop through and create array storing index of start and end of each colour'''

    row = board[y, :]

    #check if row is empty first
    if len(row[row == 0]) != 8:
        cols = [-1, 1]
        for col in cols:
            L = []
            e = 0

            #Get all start and end positions of colours
            while e < len(row):
                while row[e] != col and e < len(row):
                    e += 1

                L.append(e)
                e += 1

                while row[e] == col and e < len(row):
                    e += 1

                L.append(e)

    return 0


def analyze_cols(board, x, length):
    '''
    analyze
    '''


def analyze_diags(board, x, y, length):
    ''''''



