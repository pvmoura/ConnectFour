#!/usr/bin/env python
"""
Connect 4 for Python
"""
import sys


class HumanPlayer(object):
    def __init__(self, turn=True, name='P'):
        self.name = name
        self.turn = turn

    def check_valid_input(self, user_input, board):
        user_input = user_input.lower()
        return (user_input in
                [str(x) for x in range(1, board.columns + 1)] + ['q'])

    def move(self, board):
        # add a move function for the human
        while True:
            move = raw_input(
                self.name + "'s turn. Enter a column number to move: ")
            if self.check_valid_input(move, board):
                return move

class ComputerPlayer(object):
    def __init__(self, turn=False):
        self.name = 'C'
        self.turn = turn

    def move(self):
        # add a move function for the computer
        pass

class ConnectFour(object):
    def __init__(self, columns=7, column_size=6):
        self.board = Board(columns, column_size)

    def check_winner(self):
        return (self.board.check_horizontal() or
                self.board.check_vertical_and_diagonal())

    def read_player_move(self):
        return self.current_player.move(self.board)

    def play(self, human=True):
        players = [HumanPlayer(), HumanPlayer(False, 'Q')]
        if not human:
            players[1] = ComputerPlayer()
        self.current_player = players[0]
        while not self.check_winner():
            print self.board
            move = self.read_player_move()
            if move in ('q', 'Q'):
                sys.exit(0)
            move = int(move)
            for cell in self.board:
                if cell.col == move - 1 and cell.is_empty():
                    self.board.set_cell(cell, self.current_player.name)
                    self.current_player = self.get_next_player(players)[0]
                    break

        print self.board
        self.current_player = self.get_next_player(players)[0]
        print self.current_player.name, "won the game!"

    def get_next_player(self, players_list):
        for player in players_list:
            player.turn = not player.turn
        return [player for player in players_list if player.turn is True]


class Board(object):
    def __init__(self, columns=7, column_size=6):
        self.columns = columns
        self.column_size = column_size
        self.reset_board()
        self.direction_tuples = {
            "n": (0, 1)
            "s": (0, -1)
            "e": (1, 0)
            "w": (-1, 0)
        }

    def set_cell(self, cell, value):
        self.board[cell.row][cell.col] = value

    def reset_board(self):
        self.board = [['_' for j in range(self.columns)]
                      for i in range(self.column_size)]

    def __iter__(self, ):
        """
        """
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                yield Cell(col, row_index, col_index,
                        self.columns - 1, self.column_size - 1)

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

    def check_horizontal(self):
        # get a cell and check it's next four siblings
        # if you encounter something not like the previous
        # restart the counter and keep going
        # there's no reason to continue if you're restarting
        # the counter within 4 spots of the length of the row
        for cell in self.board:
            #check connections to right 

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

    def translate_direction_to_tuple(direction):
        tuple_list = [self.direction_tuples[direction] for direction in list(direction)]
        direction = [0, 0]
        for tup in tuple_list:
            direction[0] += tup[0]
            direction[1] += tup[1]
        return direction

    def get_connection(self, cell, direction):
        translated_direction = translate_direction_to_tuple(direction)
        row_position = translated_direction[0] + cell.row
        column_position = translate_direction[1] + cell.col
        return cell.value == self.board[row_position][column_position]

    def check_vertical_and_diagonal(self):
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
    def __init__(self, value, row_index, column_index, row_terminal, column_terminal):
        self.value = value
        self.row = row_index
        self.col = column_index
        self.connections = {}
        self.on_edge = self.is_edge(row_terminal, column_terminal)
        self.on_corner = self.is_corner(row_terminal, column_terminal)

    def __str__(self):
        return "{value} at ({row}, {col})".format(value=self.value,
                                                  row=self.row,
                                                  col=self.col)

    def is_empty(self):
        return self.value == '_'

    def is_edge(self, row_terminal, column_terminal):
        return (self.row == 0 or self.row == row_terminal or
                self.col == 0 or self.col == column_terminal)

    def is_corner(self, row_terminal, column_terminal):
        return ((self.row == 0 and self.col == 0) or
                (self.row == 0 and self.col == column_terminal) 
                (self.row == row_terminal and self.col == 0) or
                (self.row == row_terminal and self.col == column_terminal))

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
