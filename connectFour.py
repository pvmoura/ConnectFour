#!/usr/bin/env python
"""
Connect 4 for Python
"""
import sys


class ConnectFour(object):
    def __init__(self, columns=7, column_size=6):
        self.board = Board(columns, column_size)

    def checkWinner(self):
        return (self.board.checkHorizontal() or
                self.board.checkVerticalDiagonal())

    def checkValidInput(self, user_input):
        user_input = user_input.lower()
        return (user_input in
                [str(x) for x in range(1, self.board.columns + 1)] + ['q'])

    def read_player_move(self, current_player):
        while True:
            move = raw_input(
                current_player + "'s turn. Enter a column number to move: ")
            if self.checkValidInput(move):
                return move

    def play(self):
        player = 'P'
        counter = 1
        while not self.checkWinner():
            print self.board
            move = self.read_player_move(player)
            if move in ('q', 'Q'):
                sys.exit(0)
            move = int(move)
            for cell in self.board:
                if cell.col == move - 1 and cell.is_empty():
                    self.board.set_cell(cell, player)
                    player = self.next_player(player)
                    break

        print self.board
        print player, " won the game!"

    def next_player(self, player):
        if player == 'P':
            return 'C'
        elif player == 'C':
            return 'P'


class Board(object):
    def __init__(self, columns=7, column_size=6):
        self.columns = columns
        self.column_size = column_size
        self.resetBoard()

    def set_cell(self, cell, value):
        self.board[cell.row][cell.col] = value

    def resetBoard(self):
        self.board = [['_' for j in range(self.columns)]
                      for i in range(self.column_size)]

    def __iter__(self, ):
        """
        """
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                yield Cell(col, row_index, col_index)

    def __str__(self):
        columnNumbers = ""
        for i in range(self.columns + 1):
            if i != 0:
                columnNumbers += str(i) + " "
        output = "\n" + columnNumbers + "\n"
        for row in reversed(self.board):
            rowString = ""
            for elem in row:
                rowString += str(elem) + " "
            output += rowString + "\n"
        return output

    def checkHorizontal(self):
        for row in self.board:
            pw = None
            if row.count('C') >= 4:
                pw = 'C'
            elif row.count('P') >= 4:
                pw = 'P'
            if pw:
                winCounter = 1
                prev_index = 0
                for index, val in enumerate(row):
                    if val == pw:
                        if prev_index + 1 == index:
                            winCounter += 1
                        prev_index = index
                if winCounter == 4:
                    return pw
        return False

    def checkVerticalDiagonal(self):
        """
        """
        for rowIndex, row in enumerate(self.board):
            maxLength = len(self.board) - 4
            if rowIndex <= maxLength:
                for index, val in enumerate(row):
                    if val == 'C' or val == 'P':
                        if self.check_vertical_winning_condition(val,
                                                                 rowIndex,
                                                                 index):
                            return val
                        # check diagonal
                        if self.check_diagonal_winning_condition(val,
                                                                 rowIndex,
                                                                 index,
                                                                 maxLength):
                            return val
        return False

    def check_vertical_winning_condition(self, val, row_index, index):
        return (val == self.board[row_index + 1][index] and
                val == self.board[row_index + 2][index] and
                val == self.board[row_index + 3][index])

    def check_diagonal_winning_condition(self, val, row_index,
                                         index, max_length):
        return ((index <= max_length and
                 val == self.board[row_index + 1][index + 1] and
                 val == self.board[row_index + 2][index + 2] and
                 val == self.board[row_index + 3][index + 3]) or
                (index >= max_length and
                 val == self.board[row_index + 1][index - 1] and
                 val == self.board[row_index + 2][index - 2] and
                 val == self.board[row_index + 3][index - 3]))


class Cell(object):
    def __init__(self, value, row_index, column_index):
        self.value = value
        self.row = row_index
        self.col = column_index

    def __str__(self):
        return "{value} at ({row}, {col})".format(value=self.value,
                                                  row=self.row,
                                                  col=self.col)

    def is_empty(self):
        return self.value == '_'

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
