import copy
board = []
pieces = {"0" : 0, 
          "WR" : 2, "WKt" : 3, "WB" : 4, "WQ" :  5, "WK" :  6, "WP" : 7,
          "BR" :-2, "BKt" :-3, "BB" :-4, "BQ" : -5, "BK" : -6, "BP" :-7}
r_pieces = {}

WHITE = 1
BLACK = -1


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


def dump_board():
    for j in range(9, 1, -1):
        for i in range(2, 10):
            print "%4s" %r_pieces[board[i][j]],
        print 

def get_moves_WP(p):
    moves = []
    if board[p[0]][p[1] + 1] == 0:
        moves.append([p[0], p[1] + 1])
    for i in [1, -1]:
        if board[p[0] + i][p[1] + 1] >= 7:
            moves.append([p[0] + i, p[1] + 1])
    if p[1] == 3 and board[p[0]][p[1] + 1] == 0 and board[p[0]][p[1] +2] == 0:
        moves.append([p[0], p[1] + 2])
    return moves

def get_moves_BP(p):
    moves = []
    if board[p[0]][p[1] - 1] == 0:
        moves.append([p[0], p[1] - 1])
    for i in [1, -1]:
        if board[p[0] + i][p[1] - 1] >= 1 and board[p[0] + i][p[1] - 1] <= 6:
            moves.append([p[0] + i, p[1] - 1])
    if p[1] == 8 and board[p[0]][p[1] - 1] == 0 and board[p[0]][p[1] -2] == 0:
        moves.append([p[0], p[1] - 2])
    return moves

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
        if board[p[0]][p[1] + i] * colour < -2:
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

def m(square):
    row = "ABCDEFGH"
    pos = (row.find(square[0]), int(square[1]))
    return (pos[0] + 2, pos[1] + 1)

def mr(position):
    row = "ABCDEFGH"
    return "%s%d" % (row[position[0] - 2], position[1] -1)


def get_moves(position):
    for f in king_moves(WHITE, m("C6"), board):
        print mr(f),




for (k, v) in pieces.items():
    r_pieces[v] = k

board = populate_board()
dump_board()
get_moves(1)
