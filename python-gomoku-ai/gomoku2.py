import numpy as np


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

    a = score(b)

    if len(moves) == 0:
        return 4, 4

    else:
        best_move = (-1, -1)
        if col == 1:
            best_val = -100000
            for move in moves:
                b[move[0], move[1]] = col
                value = minimax(b, 1, opp, -1000000, 1000000, a, move[0], move[1])

                if value > best_val:
                    best_move = move
                    best_val = value

                b[move[0], move[1]] = 0

        else:
            best_val = 100000
            for move in moves:
                b[move[0], move[1]] = col

                value = minimax(b, 1, opp, -1000000, 1000000, a, move[0], move[1])

                if value < best_val:
                    best_move = move
                    best_val = value

                b[move[0], move[1]] = 0

    return best_move[0], best_move[1]


def minimax(board, depth, col, alpha, beta, cur_score, y, x):
    # black wants to maximize while white will want to minimize

    free_squares = get_free_squares_adj(board)
    a = adjustment(board, y, x)
    if a == 100000 or a == -100000:
        return a

    cur = cur_score + a

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
            value = minimax(board, depth - 1, -1, alpha, beta, cur, move[0], move[1])
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
            value = minimax(board, depth - 1, 1, alpha, beta, cur, move[0], move[1])
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


def score(board):
    MAX_SCORE = 100000

    open_b = [0, 0, 0, 0, 0, 0]
    semi_open_b = [0, 0, 0, 0, 0, 0]
    closed_b = [0, 0, 0, 0, 0, 0]
    open_w = [0, 0, 0, 0, 0, 0]
    semi_open_w = [0, 0, 0, 0, 0, 0]
    closed_w = [0, 0, 0, 0, 0, 0]

    for i in range(2, 6):
        open_b[i], semi_open_b[i], closed_b[i] = detect_rows(board, 1, i)
        open_w[i], semi_open_w[i], closed_w[i] = detect_rows(board, -1, i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1 or closed_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1 or closed_w[5] >= 1:
        return -MAX_SCORE


    return (-2000 * open_w[4] +
            -800 * (semi_open_w[4] + detect_repeated_twos(board, -1)) +
            -300 * (open_w[3] + detect_one_two_one(board, -1)) +
            -10 * semi_open_w[3] +
            -5 * open_w[2] +
            semi_open_w[2] +

            2000 * open_b[4] +
            800 * (semi_open_b[4] + detect_repeated_twos(board, 1)) +
            300 * (open_b[3] + detect_one_two_one(board, 1)) +
            10 * semi_open_b[3] +
            5 * open_b[2] +
            semi_open_b[2])


def adjustment(board, y, x):
    #New Score
    # upper left to bottom right
    a, b = y, x
    while a != 0 and b != 0:
        a -= 1
        b -= 1

    #upper right to bottom left
    c, d = y, x
    while c != 0 and d != 7:
        c -= 1
        d += 1

    MAX_SCORE = 100000

    new_open_b = [0, 0, 0, 0, 0, 0]
    new_semi_open_b = [0, 0, 0, 0, 0, 0]
    new_closed_b = [0, 0, 0, 0, 0, 0]
    new_open_w = [0, 0, 0, 0, 0, 0]
    new_semi_open_w = [0, 0, 0, 0, 0, 0]
    new_closed_w = [0, 0, 0, 0, 0, 0]

    for i in range(2, 6):
        a1, b1, c1 = detect_row(board, 1, y, 0, i, 0, 1)
        a2, b2, c2 = detect_row(board, 1, 0, x, i, 1, 0)
        a3, b3, c3 = detect_row(board, 1, a, b, i, 1, 1)
        a4, b4, c4 = detect_row(board, 1, c, d, i, 1, -1)

        new_open_b[i] += (a1 + a2 + a3 + a4)
        new_semi_open_b[i] += (b1 + b2 + b3 +b4)
        new_closed_b[i] += (c1 + c2 + c3 + c4)

        d1, e1, f1 = detect_row(board, -1, y, 0, i, 0, 1)
        d2, e2, f2 = detect_row(board, -1, 0, x, i, 1, 0)
        d3, e3, f3 = detect_row(board, -1, a, b, i, 1, 1)
        d4, e4, f4 = detect_row(board, -1, c, d, i, 1, -1)

        new_open_w[i] += (d1 + d2 + d3 + d4)
        new_semi_open_w[i] += (f1 + f2 + f3 + f4)
        new_closed_w[i] += (e1 + e2 + e3 + e4)

    if new_open_b[5] >= 1 or new_semi_open_b[5] >= 1 or new_closed_b[5] >= 1:
        return MAX_SCORE

    elif new_open_w[5] >= 1 or new_semi_open_w[5] >= 1 or new_closed_w[5] >= 1:
        return -MAX_SCORE

    new_score = (-2000 * new_open_w[4] +
            -800 * (new_semi_open_w[4] + detect_repeated_twos(board, -1)) +
            -300 * (new_open_w[3] + detect_one_two_one(board, -1)) +
            -10 * new_semi_open_w[3] +
            -5 * new_open_w[2] +
            new_semi_open_w[2] +

            2000 * new_open_b[4] +
            800 * (new_semi_open_b[4] + detect_repeated_twos(board, 1)) +
            300 * (new_open_b[3] + detect_one_two_one(board, 1)) +
            10 * new_semi_open_b[3] +
            5 * new_open_b[2] +
            new_semi_open_b[2])

    #Old score
    temp = board[y, x]
    board[y, x] = 0

    e, f = y, x
    while a != 0 and b != 0:
        a -= 1
        b -= 1

    g, h = y, x
    while g != 0 and h != 7:
        g -= 1
        h += 1

    open_b = [0, 0, 0, 0, 0]
    semi_open_b = [0, 0, 0, 0, 0]
    closed_b = [0, 0, 0, 0, 0]
    open_w = [0, 0, 0, 0, 0]
    semi_open_w = [0, 0, 0, 0, 0]
    closed_w = [0, 0, 0, 0, 0]

    for i in range(2, 5):
        a1, b1, c1 = detect_row(board, 1, y, 0, i, 0, 1)
        a2, b2, c2 = detect_row(board, 1, 0, x, i, 1, 0)
        a3, b3, c3 = detect_row(board, 1, e, f, i, 1, 1)
        a4, b4, c4 = detect_row(board, 1, g, h, i, 1, -1)

        open_b[i] += (a1 + a2 + a3 + a4)
        semi_open_b[i] += (b1 + b2 + b3 +b4)
        closed_b[i] += (c1 + c2 + c3 + c4)

        d1, e1, f1 = detect_row(board, -1, y, 0, i, 0, 1)
        d2, e2, f2 = detect_row(board, -1, 0, x, i, 1, 0)
        d3, e3, f3 = detect_row(board, -1, e, f, i, 1, 1)
        d4, e4, f4 = detect_row(board, -1, g, h, i, 1, -1)

        open_w[i] += (d1 + d2 + d3 + d4)
        open_w[i] += (f1 + f2 + f3 + f4)
        closed_w[i] += (e1 + e2 + e3 + e4)

    old_score = (-2000 * open_w[4] +
                 -800 * (semi_open_w[4] + detect_repeated_twos(board, -1)) +
                 -300 * (open_w[3] + detect_one_two_one(board, -1)) +
                 -10 * semi_open_w[3] +
                 -5 * open_w[2] +
                 semi_open_w[2] +

                 2000 * open_b[4] +
                 800 * (semi_open_b[4] + detect_repeated_twos(board, 1)) +
                 300 * (open_b[3] + detect_one_two_one(board, 1)) +
                 10 * semi_open_b[3] +
                 5 * open_b[2] +
                 semi_open_b[2])

    board[y, x] = temp
    return new_score - old_score


def detect_repeated_twos(board, col):
    count = 0
    # columns
    for colu in range(0, 8):
        count1 = 0
        count2 = 0
        row = 0
        while row < 8:
            if board[row, colu] == col:
                count1 += 1
                row += 1
            elif count1 == 2 and board[row, colu] == 0:
                row += 1
                break
            elif board[row, colu] != 0:
                count1 = 0
                row += 2
            else:
                count1 = 0
                row += 1

        while row < 8:
            if board[row, colu] == col:
                count2 += 1
                row += 1
            else:
                break

        if count1 == 2 and count2 == 2:
            count += 1

    # rows
    for row in range(0, 8):
        count1 = 0
        count2 = 0
        colu = 0
        while colu < 8:
            if board[row, colu] == col:
                count1 += 1
                colu += 1
            elif count1 == 2 and board[row, colu] == 0:
                colu += 1
                break
            else:
                count1 = 0
                colu += 1

        while colu < 8:
            if board[row, colu] == col:
                count2 += 1
                colu += 1
            else:
                break
        if count1 == 2 and count2 == 2:
            count += 1

            # right-left diags
    for row in range(0, 4):
        count1 = 0
        count2 = 0
        colu = 0
        while colu < 8 and row < 8:
            if board[row, colu] == col:
                count1 += 1
                row += 1
                colu += 1
            elif count1 == 2 and board[row, colu] == 0:
                colu += 1
                row += 1
                break
            else:
                count1 = 0
                row += 1
                colu += 1
        while colu < 8 and row < 8:
            if board[row, colu] == col:
                count2 += 1
                row += 1
                colu += 1
            else:
                break
        if count1 == 2 and count2 == 2:
            count += 1

    for colu in range(1, 4):
        count1 = 0
        count2 = 0
        row = 0
        while colu < 8 and row < 8:
            if board[row, colu] == col:
                count1 += 1
                row += 1
                colu += 1
            elif count1 == 2 and board[row, colu] == 0:
                colu += 1
                row += 1
                break
            else:
                count1 = 0
                row += 1
                colu += 1
        while colu < 8 and row < 8:
            if board[row, colu] == col:
                count2 += 1
                row += 1
                colu += 1
            else:
                break
        if count1 == 2 and count2 == 2:
            count += 1

            # left-right diags
    for row in range(0, 4):
        count1 = 0
        count2 = 0
        colu = 7
        while colu >= 0 and row < 8:
            if board[row, colu] == col:
                count1 += 1
                row += 1
                colu -= 1
            elif count1 == 2 and board[row, colu] == 0:
                colu -= 1
                row += 1
                break
            else:
                count1 = 0
                row += 1
                colu -= 1
        while colu >= 0 and row < 8:
            if board[row, colu] == col:
                count2 += 1
                row += 1
                colu -= 1
            else:
                break
        if count1 == 2 and count2 == 2:
            count += 1

    for colu in range(4, 7):
        count1 = 0
        count2 = 0
        row = 0
        while colu >= 0 and row < 8:
            if board[row, colu] == col:
                count1 += 1
                row += 1
                colu -= 1
            elif count1 == 2 and board[row, colu] == 0:
                colu -= 1
                row += 1
                break
            else:
                count1 = 0
                row += 1
                colu -= 1
        while colu >= 0 and row < 8:
            if board[row, colu] == col:
                count2 += 1
                row += 1
                colu -= 1
            else:
                break
        if count1 == 2 and count2 == 2:
            count += 1

    return count


def detect_one_two_one(board, col):
    count = 0
    # columns
    for colu in range(0, 8):
        if board[0, colu] == 0 and board[2, colu] == 0 and board[5, colu] == 0 and board[7, colu] == 0:
            if board[1, colu] == col and board[3, colu] == col and board[4, colu] == col and board[6, colu] == col:
                count += 1

    # rows
    for row in range(0, 8):
        if board[row, 0] == 0 and board[row, 2] == 0 and board[row, 5] == 0 and board[row, 7] == 0:
            if board[row, 1] == col and board[row, 3] == col and board[row, 4] == col and board[row, 6] == col:
                count += 1

    # right-left diags
    if board[0, 0] == 0 and board[2, 2] == 0 and board[5, 5] == 0 and board[7, 7] == 0:
        if board[1, 1] == col and board[3, 3] == col and board[4, 4] == col and board[6, 6] == col:
            count += 1

    # left-right diags
    if board[0, 7] == 0 and board[2, 5] == 0 and board[5, 2] == 0 and board[7, 0] == 0:
        if board[1, 6] == col and board[3, 4] == col and board[4, 3] == col and board[6, 1] == col:
            count += 1

    return count


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # (0,1) left to right
    if d_y == 0:
        # bordered both
        if (x_end - length + 1) == 0 and x_end == (len(board[0]) - 1):
            return "CLOSED"
        # border left
        elif (x_end - length + 1) == 0:
            if board[y_end, x_end + 1] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # border right
        elif x_end == (len(board[0]) - 1):
            if board[y_end, x_end - length] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # mid
        elif board[y_end, x_end + 1] == board[y_end, x_end - length]:
            if board[y_end, x_end + 1] == 0:
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"

    # (1,0) top to bot
    elif d_x == 0:
        # bordered both
        if y_end - length + 1 == 0 and y_end == (len(board) - 1):
            return "CLOSED"
        # border top
        elif y_end - length + 1 == 0:
            if board[y_end + 1, x_end] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # border bot
        elif y_end == (len(board) - 1):
            if board[y_end - length, x_end] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # mid
        elif board[y_end + 1, x_end] == board[y_end - length, x_end]:
            if board[y_end + 1, x_end] == 0:
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"

    # (1,1) diag up left - bot right
    elif d_x == 1:
        # bordered both
        if (x_end == (len(board[0]) - 1) and y_end - length + 1 == 0) or (
                y_end == (len(board) - 1) and x_end - length + 1 == 0):
            return "CLOSED"
        # border top left
        elif x_end - length + 1 == 0 or y_end - length + 1 == 0:
            if board[y_end + 1, x_end + 1] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # border bottom right
        elif x_end == (len(board[0]) - 1) or y_end == (len(board) - 1):
            if board[y_end - length, x_end - length] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # mid
        elif board[y_end + 1, x_end + 1] == board[y_end - length, x_end - length]:
            if board[y_end + 1, x_end + 1] == 0:
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"

    # (1,-1) diag up right - bot left
    elif d_x == -1:
        # bordered both
        if (y_end == (len(board) - 1) and (x_end + length - 1 == (len(board[0]) - 1))) or (
                x_end == 0 and (y_end - length + 1 == 0)):
            return "CLOSED"
        # border top right
        elif ((y_end - length + 1) == 0) or ((x_end + length - 1) == (len(board[0]) - 1)):
            if board[y_end + 1, x_end - 1] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # border bottom left
        elif y_end == (len(board) - 1) or x_end == 0:
            if board[y_end - length, x_end + length] == 0:
                return "SEMIOPEN"
            else:
                return "CLOSED"
        # mid
        elif board[y_end + 1, x_end - 1] == board[y_end - length, x_end + length]:
            if board[y_end + 1, x_end - 1] == 0:
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
    count = 0

    if d_y == 0:
        i = x_start
        while i < len(board[0]):
            if board[y_start, i] == col:
                count += 1
                i += 1
            else:
                if count == length:
                    x_end = i - 1
                    y_end = y_start
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1
                i += 1
                count = 0
        if count == length:
            x_end = i - 1
            y_end = y_start
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                closed_seq_count += 1

    elif d_x == 0:
        i = y_start
        while i < len(board):
            if board[i, x_start] == col:
                count += 1
                i += 1
            else:
                if count == length:
                    x_end = x_start
                    y_end = i - 1
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1
                i += 1
                count = 0
        if count == length:
            x_end = x_start
            y_end = i - 1
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                closed_seq_count += 1

    elif d_x == 1:
        i = x_start
        e = y_start
        while i < len(board[0]) and e < len(board):
            if board[e, i] == col:
                count += 1
                i += 1
                e += 1
            else:
                if count == length:
                    x_end = i - 1
                    y_end = e - 1
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1
                i += 1
                e += 1
                count = 0
        if count == length:
            x_end = i - 1
            y_end = e - 1
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                closed_seq_count += 1

    elif d_x == -1:
        i = x_start
        e = y_start
        while i >= 0 and e < len(board):
            if board[e, i] == col:
                count += 1
                i -= 1
                e += 1
            else:
                if count == length:
                    x_end = i + 1
                    y_end = e - 1
                    if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1
                    elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                        closed_seq_count += 1
                i -= 1
                e += 1
                count = 0
        if count == length:
            x_end = i + 1
            y_end = e - 1
            if is_bounded(board, y_end, x_end, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_end, x_end, length, d_y, d_x) == "CLOSED":
                closed_seq_count += 1

    return open_seq_count, semi_open_seq_count, closed_seq_count


def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
    # columns and diags
    for i in range(0, len(board[0])):
        dirs = [[1, 0], [1, 1], [1, -1]]
        for dir in dirs:
            a, b, c = detect_row(board, col, 0, i, length, dir[0], dir[1])
            open_seq_count += a
            semi_open_seq_count += b
            closed_seq_count += c
    # rows and left right diags
    for i in range(1, len(board)):
        dirs = [[0, 1], [1, 1]]
        for dir in dirs:
            a, b, c = detect_row(board, col, i, 0, length, dir[0], dir[1])
            open_seq_count += a
            semi_open_seq_count += b
            closed_seq_count += c

    # right to left diags
    for i in range(1, len(board)):
        a, b, c = detect_row(board, col, i, (len(board[0]) - 1), length, 1, -1)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c

    # top row
    a, b, c = detect_row(board, col, 0, 0, length, 0, 1)
    open_seq_count += a
    semi_open_seq_count += b
    closed_seq_count += c

    return open_seq_count, semi_open_seq_count, closed_seq_count

