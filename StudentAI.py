from random import randint
from BoardClasses import Move
from BoardClasses import Board
from math import inf
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        new_move = self.MiniMax()
        if len(new_move.seq) == 0:
            random_moves = self.board.get_all_possible_moves(self.color)
            index = randint(0, len(random_moves) - 1)
            inner_index = randint(0, len(random_moves[index]) - 1)
            random_move = random_moves[index][inner_index]
            self.board.make_move(random_move, self.color)
            return random_move
        else:
            self.board.make_move(new_move, self.color)
            return new_move

    def get_value(self, input_color):
        # add more condition
        value = 0
        count = 0
        if input_color == 1:
            color = 'B'
            for row in range(0, self.row):
                for col in range(0, self.col):
                    checker = self.board.board[row][col]
                    if checker.color == color:
                        # more weight to cornor
                        if (checker.col == 0 and checker.row == self.row-1):
                            value += 3
                        if (checker.col == self.col-1 and checker.row == self.row-1):
                            value += 3
                        if checker.is_king:
                            # not addding row num
                            # so that moving forward and backward is equal
                            value += 10
                        else:
                            value += checker.row
                            # give more weight
                            # encourage pawns to become king
                            if checker.row+1 > self.row/2:
                                value += (checker.row+1 - self.row/2)*2
                        if row == self.row - 1:
                            value += 5
                        elif col == self.col - 1 or row * col == 0:
                            value += 2
                    elif checker.color != color and checker.color != '.':
                        if checker.is_king:
                            value -= 2*(checker.row)
                            # value -= 10
                        else:
                            value -= 0.5*(checker.row)
                        if row == self.row - 1 or col == self.col - 1 or row * col == 0:
                            value -= 2
        else:
            color = 'W'
            for row in range(0, self.row):
                for col in range(0, self.col):
                    checker = self.board.board[row][col]
                    if checker.color == color:
                        # more weight to corner
                        if (checker.col == 0 and checker.row == 0):
                            value += 3
                        if (checker.col == self.col-1 and checker.row == 0):
                            value += 3
                        if checker.is_king:
                            value += 10
                        else:
                            abs_row = 8 - checker.row
                            value += abs_row
                            if abs_row > self.row/2:
                                value += (abs_row - self.row/2)*2
                        if row == 0:
                            value += 5
                        elif col == self.col - 1 or row * col == 0:
                            value += 2
                    # handle Tie
                    elif checker.color != color and checker.color != '.':
                        if checker.is_king:
                            value -= 2*(checker.row)
                            # value -= 10
                        else:
                            value -= 0.5*(checker.row)
                        if row == self.row - 1 or col == self.col - 1 or row * col == 0:
                            value -= 2
        return value

    def Cutoff(self, depth):
        return depth >= 4

    # B -> Max
    def get_MaxVal(self, depth, alpha, beta):
        color = self.color
        if self.Cutoff(depth):
            return self.get_value(self.color)
        val = -inf
        next_moves = self.board.get_all_possible_moves(color)
        for checker_index in range(0, len(next_moves)):
            for move_index in range(0, len(next_moves[checker_index])):
                next_move = next_moves[checker_index][move_index]
                self.board.make_move(next_move, color)
                val = max(val, self.get_MinVal(depth+1, alpha, beta))
                if val >= beta:
                    self.board.undo()
                    return val
                alpha = max(alpha, val)
                self.board.undo()
        return val

    def get_MinVal(self, depth, alpha, beta):
        color = self.opponent[self.color]
        if self.Cutoff(depth):
            return self.get_value(self.color)
        val = inf
        next_moves = self.board.get_all_possible_moves(color)
        for checker_index in range(0, len(next_moves)):
            for move_index in range(0, len(next_moves[checker_index])):
                next_move = next_moves[checker_index][move_index]
                self.board.make_move(next_move, color)
                val = min(val, self.get_MaxVal(depth+1, alpha, beta))
                if val <= alpha:
                    self.board.undo()
                    return val
                beta = min(beta, val)
                self.board.undo()
        return val

    def MiniMax(self):
        alpha = -inf
        beta = inf
        best_move = Move([])
        moves = self.board.get_all_possible_moves(self.color)
        for checker_index in range(0, len(moves)):
            for move_index in range(0, len(moves[checker_index])):
                move = moves[checker_index][move_index]
                if len(move) == 0:
                    pass
                depth = 0
                # *(1) start: undo later
                self.board.make_move(move, self.color)
                value = self.get_MinVal(depth+1, alpha, beta)
                if value > alpha:
                    alpha = value
                    best_move = move
                # *(1) end
                self.board.undo()
        return best_move


