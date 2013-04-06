import copy
board = []
pieces = {"0" : 0, 
          "WR" : 2, "WKt" : 3, "WB" : 4, "WQ" :  5, "WK" :  6, "WP" : 7,
          "BR" :-2, "BKt" :-3, "BB" :-4, "BQ" : -5, "BK" : -6, "BP" :-7}

piece_values = {
        "WR" : 5, "WKt" : 3, "WB" : 3, "WQ" :  9, "WK" : 999, "WP" : 1,
        "BR" :-5, "BKt" :-3, "BB" :-3, "BQ" : -9, "BK" :-999, "BP" :-1}

r_pieces = {}

WHITE = 1
BLACK = -1
MAX_DEPTH = 4


def populate_board():
    p = pieces
    board = [[-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1],
             [-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1],
             [-1, -1,   p["WR"], p["WKt"],  p["WB"], p["WQ"], p["WK"], p["WB"], p["WKt"], p["WR"],  -1, -1],
             [-1, -1,   p["WP"],  p["WP"],  p["WP"], p["WP"], p["WP"], p["WP"], p["WP"],  p["WP"],  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   0      ,        0,        0,       0,       0,       0,        0,       0,  -1, -1],
             [-1, -1,   p["BP"],  p["BP"],  p["BP"], p["BP"], p["BP"], p["BP"], p["BP"],  p["BP"],  -1, -1],
             [-1, -1,   p["BR"], p["BKt"],  p["BB"], p["BQ"], p["BK"], p["BB"], p["BKt"], p["BR"],  -1, -1],
             [-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1],
             [-1, -1,        -1,       -1,       -1,      -1,      -1,      -1,       -1,      -1,  -1, -1]]

    bt = [[i for i in range(12)] for j in range(12)]
    for i in range(12):
        for j in range(12):
            bt[i][j] = board[j][i]
    board = bt
    return board


def dump_board(board):
    for j in range(9, 1, -1):
        for i in range(2, 10):
            print "%4s" %r_pieces[board[i][j]],
        print ""

def pawn_moves(colour, p, board):
    moves = []
    if board[p[0]][p[1] + colour] == 0:
        moves.append([p[0], p[1] + colour])
    for i in [1, -1]:
        if board[p[0] + i][p[1] + colour] * colour < -2:
            moves.append([p[0] + i, p[1] + colour])

    if colour == WHITE:
        if p[1] == 3 and board[p[0]][p[1] + 1] == 0 and board[p[0]][p[1] +2] == 0:
            moves.append([p[0], p[1] + 2])
    else:
        if p[1] == 8 and board[p[0]][p[1] - 1] == 0 and board[p[0]][p[1] -2] == 0:
            moves.append([p[0], p[1] - 2])

    return moves

def rook_moves(colour, p, board):
    moves = []

    for k in (-1, 1):
        i = k
        while board[p[0]][p[1] + i] == 0:
            moves.append([p[0],p[1] + i])
            i += k
        if board[p[0]][p[1] + i] * colour < -2:
            moves.append([p[0],p[1] + i])


    for k in (-1, 1):
        i = k
        while board[p[0] + i][p[1]] == 0:
            moves.append([p[0] + i,p[1]])
            i += k
        if board[p[0] + i][p[1]] * colour < -2:
            moves.append([p[0] + i,p[1]])


    return moves

def knight_moves(colour, p, board):
    moves = []

    for i, j in [(1,2), (2,1),
                 (1,-2), (2, -1),
                 (-1,-2), (-2, -1),
                 (-1,2), (-2, 1)]:
        if board[p[0] + i][p[1] + j] * colour < -2 or \
           board[p[0] + i][p[1] + j] == 0:
               moves.append([p[0] + i,p[1] + j])

    return moves

def bishop_moves(colour, p, board):
    moves = []

    for a, b in [(1,1), (1, -1), (-1, -1), (-1, 1)]:
        i, j = (a, b)
        while board[p[0] + i][p[1] + j] == 0:
            moves.append([p[0] + i,p[1] + j])
            i += a
            j += b
        if board[p[0] + i][p[1] + j] * colour < -2:
            moves.append([p[0] + i,p[1] + j])

    return moves

def queen_moves(colour, p, board):
    moves = []
    moves.extend(bishop_moves(colour, p, board))
    moves.extend(rook_moves(colour, p, board))
    return moves

def king_moves(colour, p, board):
    moves = []
    for i,j in [(1, 0), (1, 1), 
                (0, 1), (-1, 1),
                (-1, 0), (-1, -1),
                (0, -1), (1, -1)]:
        if board[p[0] + i][p[1] + j] * colour < -2 or \
           board[p[0] + i][p[1] + j] == 0:
               moves.append([p[0] + i,p[1] + j])

    return moves

moves = {"WR"  : rook_moves}
moves = {"WR" : rook_moves, "WKt" : knight_moves, "WB" : bishop_moves,
         "WQ" : queen_moves, "WK" : king_moves, "WP" : pawn_moves,
         "BR" : rook_moves, "BKt" : knight_moves, "BB" : bishop_moves,
         "BQ" : queen_moves, "BK" : king_moves, "BP" : pawn_moves}



def m(square):
    row = "ABCDEFGH"
    pos = (row.find(square[0]), int(square[1]))
    return (pos[0] + 2, pos[1] + 1)

def mr(position):
    row = "ABCDEFGH"
    return "%s%d" % (row[position[0] - 2], position[1] -1)


def gen_moves(colour, board):
    boards = []
    for j in range(9, 1, -1):
        for i in range(2, 10):
            if not board[i][j] == 0 and board[i][j] * colour >= 2:
                for m in moves[r_pieces[board[i][j]]](colour, (i, j), board):
                    new_board = [x[:] for x in board]
                    new_board[i][j] = 0
                    new_board[m[0]][m[1]] = board[i][j] 
                    move_string = r_pieces[board[i][j]] + " " +mr((i, j))
                    boards.append((new_board, move_string))

    return boards

def evaluate(board):
    evaluation = 0
    for j in range(9, 1, -1):
        for i in range(2, 10):
            if not board[i][j] == 0:
                evaluation += piece_values[r_pieces[board[i][j]]]

    return evaluation

def play(colour, board, move_no, move_string, moves_ahead = 0):
    if moves_ahead == MAX_DEPTH:
        return (evaluate(board), board, move_string)
    new_move_no = move_no + moves_ahead
    moves_ahead += 1
    other_colour = colour * -1
    moves = []
    for m in gen_moves(colour, board):
        board = m[0]
        move = m[1]
        new_move_string = move_string
        if colour == WHITE:
            new_move_string += "%d: " % (new_move_no / 2 + 1) + move + ", "
        else:
            new_move_string += move + "\n"

        if moves_ahead == 1:
            j = list(play(other_colour, board, move_no, new_move_string, moves_ahead))
            j.append(board)
            moves.append(j)
        else:
            moves.append(play(other_colour, board, move_no, new_move_string, moves_ahead))

    if colour == WHITE:
        return max(moves, key = lambda i : i[0])
    else:
        return min(moves, key = lambda i : i[0])




for (k, v) in pieces.items():
    r_pieces[v] = k

board = populate_board()
dump_board(board)
# print evaluate(board)
b1 = board
colour = WHITE
move = 0
for i in range(6):
    move += 1
    e, b, s, b1 = play(colour,b1,move, "")
    colour *= -1
    dump_board(b1)
    print s
    print 
