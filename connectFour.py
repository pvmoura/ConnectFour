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

    def move(self, ):
        # add a move function for the computer
        pass

class ConnectFour(object):
    def __init__(self, columns=7, column_size=6):
        self.board = Board(columns, column_size)

    def read_player_move(self, ):
        return self.current_player.move(self.board)

    def play(self, human=True):
        players = [HumanPlayer(), HumanPlayer(False, 'Q')]
        if not human:
            players[1] = ComputerPlayer()
        self.current_player = players[0]
        while not self.board.check_for_win():
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
        self.initialize_board()
        self.direction_tuples = {
            "n": (1, 0),
            "s": (-1, 0),
            "e": (0, 1),
            "w": (0, -1)
        }

    def __iter__(self, ):
        """
        """
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                yield Cell(col, row_index, col_index,
                        self.columns - 1, self.column_size - 1)

    def __str__(self, ):
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

    def initialize_board(self, place_holder='_'):
        #self.board = [[ Cell('_', j, i, self.columns - 1, self.column_size - 1)
                #for j in range(self.columns)]
                #for i in range(self.column_size)]
        self.board = [[ place_holder for j in range(self.columns)]
                        for i in range(self.column_size)]

    def search_for_win(self, cell, direction, row_change=0, col_change=0):
        winCounter = 1
        while self.get_connection(cell, direction) and winCounter <= 4:
            cell = Cell(
                cell.value, cell.row + row_change, cell.col + col_change)
            winCounter += 1
        if winCounter == 4:
            return True
        return False

    def check_for_win(self, ):
        for cell in self:
            if not cell.is_empty():
                if (self.search_for_win(cell, "e", 0, 1) or
                    self.search_for_win(cell, "n", 1, 0) or
                    self.search_for_win(cell, "ne", 1, 1) or
                    self.search_for_win(cell, "se", -1, 1)):
                    return True
        return False

    def translate_direction_to_list(self, direction):
        tuple_list = [self.direction_tuples[direction] for direction in list(direction)]
        direction = [0, 0]
        for tup in tuple_list:
            direction[0] += tup[0]
            direction[1] += tup[1]
        return direction

    def get_connection(self, cell, direction):
        translated_direction = self.translate_direction_to_list(direction)
        row_position = translated_direction[0] + cell.row
        column_position = translated_direction[1] + cell.col
        if (row_position >= 0 and column_position >= 0 and
            row_position < self.column_size and column_position < self.columns):
            return not cell.is_empty() and cell.value == self.board[row_position][column_position]
        else:
            return None

class Cell(object):
    def __init__(self, value, row_index, column_index, row_terminal=6, column_terminal=5):
        self.value = value
        self.row = row_index
        self.col = column_index
        self.connections = {}
        self.on_edge = self.is_edge(row_terminal, column_terminal)
        self.on_corner = self.is_corner(row_terminal, column_terminal)

    def __str__(self, ):
        return "{value} at ({row}, {col})".format(value=self.value,
                                                  row=self.row,
                                                  col=self.col)

    def is_empty(self, ):
        return self.value == '_'

    def is_edge(self, row_terminal, column_terminal):
        return (self.row == 0 or self.row == row_terminal or
                self.col == 0 or self.col == column_terminal)

    def is_corner(self, row_terminal, column_terminal):
        return ((self.row == 0 and self.col == 0) or
                (self.row == 0 and self.col == column_terminal) or
                (self.row == row_terminal and self.col == 0) or
                (self.row == row_terminal and self.col == column_terminal))

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
