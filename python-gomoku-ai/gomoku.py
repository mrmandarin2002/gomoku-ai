#Two hundred too many if-statements

'''
still need to implement:
    detect open and broken threes 
    scoring 
    actually moving :D
'''

'''
http://www.cs.toronto.edu/~guerzhoy/180/proj/proj2/gomoku.pdf

* Submission deadline: April 2 

* I will run the tournament on Google Colab https://colab.research.google.com/ , with a GPU enabled

* Time limit on moves: 0.2 seconds on the Google Collab server

* RAM limit: 1 GB (basically, don't hog the RAM)

* Format: provide a Python function move(board, col) that returns a tuple (move_y, move_x) for colour col

* Each pair of players will play two games, starting from the same random position. Player A will play black once and white once.

* You can submit by yourself or in a team of two
'''

'''
minimax algorithm https://www.youtube.com/watch?v=l-hh51ncgDI  
function minimax(position, depth, alpha, beta, maximizingPlayer)
    if depth == 0 pr game over in positiona
        return static evaluation of position
    if maximizing Player
        maxEval = -infinity
        for each child of position 
            eval = minimax(child, depth - 1, alpha, beta, false)
            maxEval = max(MaxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha
                break
        return maxEval
    else
        mineval = +infinity
        for each child of position
            eval = minimax(child, depth-1, true)
            minEval = min(minEval, eval)
            beta = min(beta, eval)if beta <= alpha
                break
Can prune moves that are not likely 
'''

'''
Gomoku notes:
First 10 moves are important, black moves first, 5 stones exactly
Fork - create 2 semi-open 4s (4x4), 4 and semi open 3 (4x3), 2 open 3 (3x3)
Surewins - Cannot defend once in position, must use wisely not just take 3s and 4s

https://sortingsearching.com/2020/05/18/gomoku.html#introduction
http://gomokuworld.com/gomoku/1
https://lib.dr.iastate.edu/cgi/viewcontent.cgi?article=1491&context=creativecomponents 
'''

def move(board, col):
    if col == "b":
        opp = "w"
    else:
        opp = "b"
    
    moves = get_free_squares(board)

    if len(moves) == 64:
        return(4, 4)
    else:
        best_move = (-1, -1)
        if col == "b":
            best_val = -100000
            for move in moves:
                board[move[0]][move[1]] = col

                value = minimax(board, 1, opp)

                if value > best_val:
                    best_move = move
                    best_val = value

                board[move[0]][move[1]] = " "
        else:
            best_val = 100000
            for move in moves:
                board[move[0]][move[1]] = col

                value = minimax(board, 1, opp)
                if value < best_val:
                    best_move = move
                    best_val = value
                board[move[0]][move[1]] = " "

    return best_move

def minimax(board, depth, col):
    #black wants to maximize while white will want to minimize

    free_squares = get_free_squares(board)
    cur = score(board)
    if cur == 100000 or cur == -100000:
        return cur
    
    if len(free_squares) == 0:
        return 0
    
    if depth == 0:
        return cur

    if col == "b":
        best = -1000000
        for move in free_squares:
            board[move[0]][move[1]] = "b"
            best = max(best, minimax(board, depth - 1, "w"))
            board[move[0]][move[1]] = " "
        return best

    else: 
        best = 1000000
        for move in get_free_squares(board):
            board[move[0]][move[1]] = "w"
            best = min(best, minimax(board, depth - 1, "b"))
            board[move[0]][move[1]] = " "
        return best

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    closed_b = {}
    open_w = {}
    semi_open_w = {}
    closed_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i], closed_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i], closed_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1 or closed_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1 or closed_w[5] >= 1:
        return -MAX_SCORE

    '''
    still working on scoring the board 
    threat types:
        winning are fives and open fours -> D energy
        forcing are simple fours, open threes and broken threes -> must attacc and defend
    '''

    return (-2000 * open_w[4] +
            -800 * (semi_open_w[4] + detect_repeated_twos(board, "w"))+
            -300 * (open_w[3] + detect_one_two_one(board, "w")) +
            -10 * semi_open_w[3] +
            -5 * open_w[2] +
            semi_open_w[2] +

            2000 * open_b[4] +
            800 * (semi_open_b[4] + detect_repeated_twos(board, "b"))+
            300 * (open_b[3] + detect_one_two_one(board, "b")) +
            10 * semi_open_b[3] +
            5 * open_b[2] +
            semi_open_b [2])

def detect_repeated_twos(board, col):
    count = 0
    #columns 
    for colu in range(0, 8):
        count1 = 0
        count2 = 0
        row = 0
        while row < 8:
            if board[row][colu] == col:
                count1 += 1
                row += 1
            elif count1 == 2 and board[row][colu] == " ":
                row += 1
                break
            elif board[row][colu] != " ":
                count1 = 0 
                row += 2
            else: 
                count1 = 0 
                row += 1

        while row < 8:
            if board[row][colu] == col:
                count2  += 1
                row += 1
            else:
                break
        
        if count1 == 2 and count2 == 2:
            count += 1
        
    #rows
    for row in range(0, 8):
        count1 = 0
        count2 = 0
        colu = 0
        while colu < 8:
            if board[row][colu] == col:
                count1 += 1
                colu += 1
            elif count1 == 2 and board[row][colu] == " ":
                colu += 1
                break
            else: 
                count1 = 0 
                colu += 1

        while colu < 8:
            if board[row][colu] == col:
                count2  += 1
                colu += 1
            else:
                break
        if count1 == 2 and count2 == 2:
            count += 1     

    #right-left diags
    for row in range(0, 4):
        count1 = 0
        count2 = 0
        colu = 0
        while colu < 8 and row <8:
            if board[row][colu] == col:
                count1 += 1
                row += 1
                colu += 1
            elif count1 == 2 and board[row][colu] == " ":
                colu += 1 
                row += 1 
                break 
            else: 
                count1 = 0
                row += 1
                colu += 1
        while colu < 8 and row <8:
            if board[row][colu] == col:
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
        while colu < 8 and row <8:
            if board[row][colu] == col:
                count1 += 1
                row += 1
                colu += 1
            elif count1 == 2 and board[row][colu] == " ":
                colu += 1 
                row += 1 
                break 
            else: 
                count1 = 0
                row += 1
                colu += 1
        while colu < 8 and row <8:
            if board[row][colu] == col:
                count2 += 1
                row += 1
                colu += 1
            else:
                break 
        if count1 == 2 and count2 == 2:
            count += 1  

    #left-right diags
    for row in range(0, 4):
        count1 = 0
        count2 = 0
        colu = 7
        while colu >= 0  and row < 8:
            if board[row][colu] == col:
                count1 += 1
                row += 1
                colu -= 1
            elif count1 == 2 and board[row][colu] == " ":
                colu -= 1 
                row += 1 
                break 
            else: 
                count1 = 0
                row += 1
                colu -= 1
        while colu >= 0 and row < 8:
            if board[row][colu] == col:
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
            #print("COLU: ", colu)
            if board[row][colu] == col:
                count1 += 1
                row += 1
                colu -= 1
            elif count1 == 2 and board[row][colu] == " ":
                colu -= 1 
                row += 1 
                break 
            else: 
                count1 = 0
                row += 1
                colu -= 1
        while colu >= 0 and row < 8:
            if board[row][colu] == col:
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
    #columns 
    for colu in range(0, 8):
        if board[0][colu] == " " and board[2][colu] == " " and board[5][colu] == " " and board[7][colu] == " ":
            if board[1][colu] == col and board[3][colu] == col and board[4][colu] == col and board[6][colu] == col:
                count += 1

    #rows
    for row in range(0, 8):
        if board[row][0] == " " and board[row][2] == " " and board[row][5] == " " and board[row][7] == " ":
            if board[row][1] == col and board[row][3] == col and board[row][4] == col and board[row][6] == col:
                count += 1

    #right-left diags
    if board[0][0] == " " and board[2][2] == " " and board[5][5] == " " and board[7][7] == " ":
        if board[1][1] == col and board[3][3] == col and board[4][4] == col and board[6][6] == col:
            count += 1

    #left-right diags
    if board[0][7] == " " and board[2][5] == " " and board[5][2] == " " and board[7][0] == " ":
        if board[1][6] == col and board[3][4] == col and board[4][3] == col and board[6][1] == col:
            count += 1

    return count

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # (0,1) left to right
    if d_y == 0:
        #bordered both
        if (x_end - length + 1) == 0 and x_end == (len(board[0]) - 1):
            return "CLOSED"
        #border left
        elif (x_end - length + 1) == 0:
            if board[y_end][x_end + 1] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #border right
        elif x_end == (len(board[0]) - 1):
            if board[y_end][x_end - length] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #mid
        elif board[y_end][x_end + 1] == board[y_end][x_end - length]:
            if board[y_end][x_end + 1] == " ":
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"

    #(1,0) top to bot
    elif d_x == 0:
        #bordered both
        if y_end - length + 1 == 0 and y_end == (len(board) - 1):
            return "CLOSED"
        #border top
        elif y_end - length + 1 == 0:
            if board[y_end + 1][x_end] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #border bot
        elif y_end == (len(board) - 1):
            if board[y_end - length][x_end] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #mid
        elif board[y_end + 1][x_end] == board[y_end - length][x_end]:
            if board[y_end + 1][x_end] == " ":
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"

    #(1,1) diag up left - bot right
    elif d_x == 1:
        #bordered both
        if (x_end == (len(board[0]) - 1) and y_end - length + 1 == 0) or (y_end == (len(board) - 1) and x_end - length + 1 == 0):
            return "CLOSED"
        #border top left
        elif x_end - length + 1 == 0 or y_end - length + 1 == 0:
            if board[y_end + 1][x_end + 1] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #border bottom right
        elif x_end == (len(board[0]) - 1) or y_end == (len(board) - 1):
            if board[y_end - length][x_end - length] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #mid
        elif board[y_end + 1][x_end + 1] == board[y_end - length][x_end - length]:
            if board[y_end + 1][x_end + 1] == " ":
                return "OPEN"
            else:
                return "CLOSED"
        else:
            return "SEMIOPEN"

    #(1,-1) diag up right - bot left
    elif d_x == -1:
        #bordered both
        if (y_end == (len(board) - 1) and (x_end + length - 1 == (len(board[0]) - 1))) or (x_end == 0 and (y_end - length + 1 == 0)):
            return "CLOSED"
        #border top right
        elif ((y_end - length + 1) == 0) or ((x_end + length - 1) == (len(board[0]) - 1)):
            if board[y_end + 1][x_end - 1] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #border bottom left
        elif y_end == (len(board) - 1) or x_end == 0:
            if board[y_end - length][x_end + length] == " ":
                return "SEMIOPEN"
            else:
                return "CLOSED"
        #mid
        elif board[y_end + 1][x_end - 1] == board[y_end - length][x_end + length]:
            if board[y_end + 1][x_end - 1] == " ":
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
            if board[y_start][i] == col:
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
            if board[i][x_start] == col:
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
            if board[e][i] == col:
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
            if board[e][i] == col:
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
    #columns and diags
    for i in range(0, len(board[0])):
        dirs = [[1, 0], [1, 1], [1, -1]]
        for dir in dirs:
            a, b, c = detect_row(board, col, 0, i, length, dir[0], dir[1])
            open_seq_count += a
            semi_open_seq_count += b
            closed_seq_count += c
    #rows and left right diags
    for i in range(1, len(board)):
        dirs = [[0, 1], [1, 1]]
        for dir in dirs:
            a, b, c = detect_row(board, col, i, 0, length, dir[0], dir[1])
            open_seq_count += a
            semi_open_seq_count += b
            closed_seq_count += c

    #right to left diags
    for i in range(1, len(board)):
        a, b, c = detect_row(board, col, i, (len(board[0]) - 1), length, 1, -1)
        open_seq_count += a
        semi_open_seq_count += b
        closed_seq_count += c
    #top row
    a, b, c = detect_row(board, col, 0, 0, length, 0, 1)
    open_seq_count += a
    semi_open_seq_count += b
    closed_seq_count += c

    return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_win(board, col, y_start, x_start, d_y, d_x):
    count = 0

    if d_y == 0:
        i = x_start
        while i < len(board[0]):
            if board[y_start][i] == col:
                count += 1
                i += 1
            else:
                if count >= 5:
                    return True
                i += 1
                count = 0
        if count >= 5:
            return True

    elif d_x == 0:
        i = y_start
        while i < len(board):
            if board[i][x_start] == col:
                count += 1
                i += 1
            else:
                if count >= 5:
                    return True
                i += 1
                count = 0
        if count >= 5:
            return True

    elif d_x == 1:
        i = x_start
        e = y_start
        while i < len(board[0]) and e < len(board):
            if board[e][i] == col:
                count += 1
                i += 1
                e += 1
            else:
                if count >= 5:
                    return True
                i += 1
                e += 1
                count = 0
        if count >= 5:
            return True

    elif d_x == -1:
        i = x_start
        e = y_start
        while i >= 0 and e < len(board):
            if board[e][i] == col:
                count += 1
                i -= 1
                e += 1
            else:
                if count >= 5:
                    return True
                i -= 1
                e += 1
                count = 0
        if count >= 5:
            return True

    return False

def get_free_squares(board):
    free_spaces = []
    for i in range(len(board)):
        for e in range(len(board[0])):
            if board[i][e] == " ":
                free_spaces.append([i, e])
    return free_spaces

def is_empty(board):
    for i in range(len(board)):
        for e in range(len(board[i])):
            if board[i][e] != " ":
                return False
    return True