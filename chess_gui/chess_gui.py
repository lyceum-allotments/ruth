#! /usr/bin/env python

# TODO
# Load sprite pictures -- DONE
# Glow behind player to move -- DONE
# Change move to be [source, destination] -- DONE
# Change eval function to maximise number of attacked squares
# Work out time for move
# Can't move into check
# Pass message when you're in checkmate
# Put bot into thread
# Highlight squares you can move to
# Witty comments when piece taken
# Player biographies

import cocos
import ruth
import time
import sys

window = [1280, 800]

#States
PIECE_SELECT = 1
MOVE_SELECT = 2
WAIT_ON_MOVE = 3

sprites = {"WR" : "white/rook.png", "WKt" : "white/knight.png", "WB" : "white/bishop.png",
         "WQ" : "white/queen.png", "WK" : "white/king.png", "WP" : "white/pawn.png",
         "BR" : "black/rook.png", "BKt" : "black/knight.png", "BB" : "black/bishop.png",
         "BQ" : "black/queen.png", "BK" : "black/king.png", "BP" : "black/pawn.png"}


def ruth_play(colour, board):
    e, b, s, b1 = ruth.play(colour,board,0)
    if e > 800:
        print "Looks like white wins!"
    if e < -800:
        print "Looks like black wins!"



    return b1




RUTH = 1
THOR = 2
DARTAGNAN = 3
JOSHUA = 4
PANDA = 5
KAT = 6
AGENT = 7 

play_fns = {RUTH : ruth_play,
           THOR : None,
           DARTAGNAN : None,
           JOSHUA  : None,
           PANDA   : None,
           KAT     : None,
           AGENT   : None}

icon_paths = {RUTH : "ruth.png",
              THOR : "thor.png",
              DARTAGNAN : "dartagnan.png",
              JOSHUA : "joshua.png",
              PANDA  : "panda.png",
              KAT    : "kat.png",
              AGENT  : "agent.png"}


class ChessGui(cocos.layer.Layer):
    is_event_handler = True

    players = [RUTH, THOR]

    def __init__(self, players):
        self.players = players
        super(ChessGui, self).__init__()
        background_sprite = cocos.sprite.Sprite("background.png")
        xwin, ywin = cocos.director.director.get_window_size()
        background_sprite.x = xwin/2
        background_sprite.y = ywin/2
        self.add(background_sprite, z=0)

        side_bar = cocos.sprite.Sprite("side_bar.png")
        side_bar.x = side_bar.width/2
        side_bar.y = side_bar.height/2 
        self.add(side_bar, z=2)

        self.board_sprite = cocos.sprite.Sprite("board.png")
        board = self.board_sprite
        board.x = 439.489   + board.width / 2.# 439.489
        board.y = 208 + board.height / 2.# 208.518
        self.allowed_moves = []

        self.add(board, z=3)
        self.init_pieces()
        self.load_icons()



    def init_pieces(self):

        self.pieces = {"WR" : [cocos.sprite.Sprite("white/rook.png") for i in range(2)],
                       "WKt" : [cocos.sprite.Sprite("white/knight.png") for i in range(2)],
                       "WB" : [cocos.sprite.Sprite("white/bishop.png") for i in range(2)],
                       "WQ" : [cocos.sprite.Sprite("white/queen.png") for i in range(8)],
                       "WK" : [cocos.sprite.Sprite("white/king.png") for i in range(1)],
                       "WP" : [cocos.sprite.Sprite("white/pawn.png")for i in range(8)],
                       "BR" : [cocos.sprite.Sprite("black/rook.png") for i in range(2)],
                       "BKt" : [cocos.sprite.Sprite("black/knight.png") for i in range(2)],
                       "BB" : [cocos.sprite.Sprite("black/bishop.png") for i in range(2)],
                       "BQ" : [cocos.sprite.Sprite("black/queen.png") for i in range(8)],
                       "BK" : [cocos.sprite.Sprite("black/king.png") for i in range(1)],
                       "BP" : [cocos.sprite.Sprite("black/pawn.png") for i in range(8)]}

        for k, v in self.pieces.items():
            for s in v:
                self.add(s, z=5)

        self.show_board(ruth.populate_board())
        self.colour = ruth.WHITE
        self.state = PIECE_SELECT

        self.glows = [range(8) for i in range(8)]
        for j in range(8):
            for i in range(8):
               glowsprite = cocos.sprite.Sprite("glow.png")
               self.glows[i][j] = glowsprite
               glowsprite.x = 456.393 + glowsprite.width/2. + (i) * 60 
               glowsprite.y = 224.6 + glowsprite.height/2. + (j) * 60
               self.add(glowsprite, z = 4)
               glowsprite.visible = False








    def load_icons(self):
        self.player_sprites = [cocos.sprite.Sprite(icon_paths[self.players[0]]),
                               cocos.sprite.Sprite(icon_paths[self.players[1]])]

        self.player_sprites[0].x = 200.500 + self.player_sprites[0].width/2
        self.player_sprites[0].y = 25.500 + self.player_sprites[0].height/2


        self.player_sprites[1].x = 1026.500 + self.player_sprites[1].width/2
        self.player_sprites[1].y = 501.500 + self.player_sprites[1].height/2


        self.add(self.player_sprites[0], z=2)
        self.add(self.player_sprites[1], z=2)

        self.glow_sprites = [cocos.sprite.Sprite(icon_paths[self.players[0]][:-4] + "_glow.png"),
                             cocos.sprite.Sprite(icon_paths[self.players[1]][:-4] + "_glow.png")]

        self.glow_sprites[0].x = 103.557 + self.glow_sprites[0].width /2
        self.glow_sprites[0].y = -75.304 + self.glow_sprites[0].height /2
        self.add(self.glow_sprites[0], z = 1)

        self.glow_sprites[1].x = 929.109 + self.glow_sprites[1].width / 2
        self.glow_sprites[1].y = 391.629 + self.glow_sprites[1].height / 2
        self.add(self.glow_sprites[1], z = 1)
        self.glow_sprites[1].visible = False

        


    def show_board(self, board):
        self.board = board
        pcs = {}
        [pcs.__setitem__(k, v[:]) for k, v in self.pieces.items()]
        for j in range(9, 1, -1):
            for i in range(2, 10):
                if not board[i][j] == 0:
                    pc = pcs[ruth.r_pieces[board[i][j]]].pop()
                    pc.x = 484.351 + 30 + (i - 2) * 60 
                    pc.y = 252.558 + 30 + (j - 2) * 60
        for v in pcs.values():
            for s in v:
                s.x = -10000


    def update_screen(self, dt):
        self.show_board(self.board)
        

    def call_bot(self, dt):
        colour_index = {ruth.WHITE : 0, ruth.BLACK : 1}[self.colour]
        play_fn = play_fns[self.players[colour_index]]
        if not play_fn == None:
            self.state = WAIT_ON_MOVE
            tick = time.time()
            self.board = play_fn(self.colour, self.board)
            tock = time.time()
            print ruth.prob_tree_size
            ruth.prob_tree_size = 0 

            print "Time for move : %d" % (tock - tick)
            self.colour *= -1
            colour_index = {ruth.WHITE : 0, ruth.BLACK : 1}[self.colour]
            self.glow_sprites[colour_index].visible = True
            self.glow_sprites[colour_index - 1].visible = False 

        self.state = MOVE_SELECT




    def on_mouse_press(self, x, y, buttons, modifiers):
        if x >= 484 and x <= 960 and y >= 252 and y <= 731:

            i = int((x - 484) / 60) + 2
            j = int((y - 252) / 60) + 2


            if (self.state == MOVE_SELECT or self.state == PIECE_SELECT) and self.board[i][j] * self.colour >= 2:

                for m in self.allowed_moves:
                    self.glows[m[2]-2][m[3]-2].visible = False
                    
                self.allowed_moves = ruth.moves[ruth.r_pieces[self.board[i][j]]](self.colour, (i, j), self.board)

                for m in self.allowed_moves:

                    new_board = [x[:] for x in self.board]
                    ruth.make_move(m, self.colour, new_board)

                    king_pos = ruth.find_piece(new_board, ruth.pieces["WK"] * self.colour)
                    # self.glows[m[2]-2][m[3]-2].visible = True
                    if king_pos in ruth.attacked_squares(self.colour * -1, new_board):
                        self.allowed_moves.remove(m)


                for m in self.allowed_moves:
                        self.glows[m[2]-2][m[3]-2].visible = True
                self.state = MOVE_SELECT
                self.selected_piece = self.board[i][j]
                self.selected_piece_pos = [i,j]


            if self.state == MOVE_SELECT: # and self.board[i][j] * self.colour >= 2:
                for k in self.allowed_moves:
                    if [i, j] == k[2:4]:
                        ruth.make_move(k, self.colour, self.board)
                        # self.board[i][j] = self.selected_piece
                        # self.board[self.selected_piece_pos[0]][self.selected_piece_pos[1]] = 0

                        self.state = PIECE_SELECT
                        self.colour *= -1
                        colour_index = {ruth.WHITE : 0, ruth.BLACK : 1}[self.colour]
                        self.glow_sprites[colour_index].visible = True
                        self.glow_sprites[colour_index - 1].visible = False 
                        self.show_board(self.board)
                        for m in self.allowed_moves:
                            self.glows[m[2]-2][m[3]-2].visible = False

                        self.allowed_moves = []




class ruth_tester(object):
    board = ruth.populate_board()
    colour = ruth.WHITE
    move = 0

    def __init__(self):
        pass

    def test_ruth(self,dt):
          # dump_board(board)
          # print evaluate(board)
          b1 = self.board
          
          
          
          colour = self.colour
          "Plie: %d" % (self.move + 1)
          self.move += 1
          tick = time.time()
          e, b, s, b1 = ruth.play(colour,b1,self.move)
          tock = time.time()
          print "Time for move: %d" % (tock - tick)
          self.colour *= -1
          gui.show_board(b1)
          self.board = b1
     

if __name__ == "__main__":
    cocos.director.director.init(window[0], window[1]) # , resizable=True)

    p1 = sys.argv[1].lower()
    p2 = sys.argv[2].lower()

    pa = [DARTAGNAN, THOR]
    for (i, v) in icon_paths.items():
        if v[:-4] == p1:
            pa[0] = i
        if v[:-4] == p2:
            pa[1] = i

    gui = ChessGui(pa)
    main_scene = cocos.scene.Scene(gui)

    rt = ruth_tester()
    main_scene.schedule(gui.update_screen)
    main_scene.schedule_interval(gui.call_bot, 1)
    # main_scene.schedule(rt.test_ruth)
    cocos.director.director.run(main_scene)
