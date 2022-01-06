from . import *
import random


class Checkers:
    def __init__(self):
        self.framespeed = 4
        self.frames = []
        # w = white, r = red, e = empty, i = illegal
        # 9x9 board!
        self.pieces = 36
        self.move = "w"
        self.board = [["w", "i", "w", "i", "e", "i", "r", "i", "r"],
                      ["i", "w", "i", "w", "i", "r", "i", "r", "i"],
                      ["w", "i", "w", "i", "e", "i", "r", "i", "r"],
                      ["i", "w", "i", "w", "i", "r", "i", "r", "i"],
                      ["w", "i", "w", "i", "e", "i", "r", "i", "r"],
                      ["i", "w", "i", "w", "i", "r", "i", "r", "i"],
                      ["w", "i", "w", "i", "e", "i", "r", "i", "r"],
                      ["i", "w", "i", "w", "i", "r", "i", "r", "i"],
                      ["w", "i", "w", "i", "e", "i", "r", "i", "r"]]
        self.jump_priority = 4  # higher than the more likely to take a jump if it is there

    def get_moves(self, color):
        moves = []
        for x in range(0, 9):
            for y in range(0, 9):
                if color == self.board[x][y]:
                    # check forward
                    # -1 if black, 1 if white
                    dir = int(2*(int(color == "w")-0.5))

                    opp_color = "w"
                    if color == "w":
                        opp_color = "r"
                    if y+dir > 8 or y+dir < 0:
                        continue
                    if x > 0:
                        if self.board[x-1][y+dir] == "e":
                            moves.append(((x, y), (x-1, y+dir)))
                        if x > 1:
                            if y+dir < 7:
                                if self.board[x-1][y+dir] == opp_color and self.board[x-2][y+2*dir] == "e":
                                    for i in range(0, self.jump_priority):
                                        moves.append(((x, y), (x-2, y+2*dir)))
                    if x < 8:
                        if self.board[x+1][y+dir] == "e":
                            moves.append(((x, y), (x+1, y+dir)))
                        if x < 7:
                            if y + dir < 7:
                                if self.board[x+1][y+dir] == opp_color and self.board[x+2][y+2*dir] == "e":
                                    for i in range(0, self.jump_priority):
                                        moves.append(((x, y), (x+2, y+2*dir)))

        return moves

    def render_frame(self):
        frame = Frame(grid=[[0 for x in range(9)] for y in range(9)])

        for x in range(0, 9):
            for y in range(0, 9):
                color = 0
                if self.board[x][y] == "w":
                    color = 3
                elif self.board[x][y] == "r":
                    color = 120
                frame.set_value((x, y), color)
        return frame

    def compile(self):
        self.frames.append(self.render_frame())
        # do moves consecutively
        self.has_move = True
        while self.pieces > 0 and self.has_move:
            moves = self.get_moves(self.move)

            if len(moves) == 0:
                self.has_move = False
                break
            pick = random.randint(0, len(moves)-1)

            mov = moves[pick]

            # update board and render Frame
            self.board[mov[0][0]][mov[0][1]] = "e"
            self.board[mov[1][0]][mov[1][1]] = self.move
            if abs(mov[0][0]-mov[1][0]) == 2:
                inner_x = int((mov[0][0] + mov[1][0])/2)
                inner_y = int((mov[0][1] + mov[1][1]) / 2)
                self.board[inner_x][inner_y] = "e"
            self.frames.append(self.render_frame())

            if self.move == "w":
                self.move = "r"
            else:
                self.move = "w"
