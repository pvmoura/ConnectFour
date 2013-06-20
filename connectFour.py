#!/usr/bin/env python
"""
Connect 4 for Python
"""
import sys
import random


class HumanPlayer(object):
    def __init__(self, turn=True, name='P', current_board=None):
        self.name = name
        self.turn = turn
        self.current_board = current_board

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
    def __init__(self, turn=False, current_board=None, opponent_name='P'):
        self.name = 'C'
        self.turn = turn
        self.current_board = current_board
        self.opponent = opponent_name

    def move(self, board):
        # add a move function for the computer
        self.current_board = board
        possible_moves = self.current_board.list_possible_moves()
        possible_move = self.check_for_winning_move(board, possible_moves)
        if possible_move:
            return possible_move[1] + 1
        return possible_moves[random.randint(0, len(possible_moves) - 1)][1] + 1

    def evaluate_board_utility(self, board):
        # evaluate the current board position based on a set of heuristics, return a value
        possible_moves = board.list_possible_moves()
        for move in possible_moves:
            pass
            #if board.count_sets_of_adjacent_checkers()
        return True

    def check_for_winning_move(self, board, possible_moves):
        cell_list = list(board)
        new_board = Board(cell_list)
        for move in possible_moves:
            new_board.board[move[0]][move[1]].value = self.opponent
            if new_board.check_for_win():
                return move
            new_board.board[move[0]][move[1]].value = self.name
            if new_board.check_for_win():
                return move
            new_board.board[move[0]][move[1]].value = '_'
        return new_board.check_for_win()



class ConnectFour(object):
    def __init__(self, cell_list=None, columns=7, column_size=6):
        self.board = Board()

    def read_player_move(self, ):
        return self.current_player.move(self.board)

    def play(self, human=False):
        players = [HumanPlayer(), HumanPlayer(False, 'Q')]
        if not human:
            players[1] = ComputerPlayer()
        self.current_player = players[0]
        while not self.board.check_for_win():
            print self.board
            move = self.read_player_move()
            if move in ('q', 'Q'):
                sys.exit(0)
            move = int(move) - 1
            possible_moves = self.board.list_possible_moves()
            position = [elem for elem in possible_moves if elem[1] == move]
            self.board.set_cell(position[0], self.current_player.name)
            self.current_player = self.get_next_player(players)[0]

        print self.board
        self.current_player = self.get_next_player(players)[0]
        print self.current_player.name, "won the game!"

    def get_next_player(self, players_list):
        for player in players_list:
            player.turn = not player.turn
        return [player for player in players_list if player.turn is True]


class Board(object):
    def __init__(self, cell_list=None, columns=7, column_size=6):
        self.columns = columns
        self.column_size = column_size
        if not cell_list:
            self.initialize_board()
        else:
            self.create_board(cell_list)
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
                #yield Cell(col, row_index, col_index,
                        #self.columns - 1, self.column_size - 1)
                yield col

    def __str__(self, ):
        columnNumbers = ""
        for i in range(self.columns + 1):
            if i != 0:
                columnNumbers += str(i) + " "
        output = "\n" + columnNumbers + "\n"
        for row in reversed(self.board):
            rowString = ""
            for elem in row:
                rowString += str(elem.value) + " "
            output += rowString + "\n"
        return output

    def initialize_board(self, place_holder='_'):
        self.board = [[ Cell('_', i, j, self.columns - 1, self.column_size - 1)
                for j in range(self.columns)]
                for i in range(self.column_size)]

    def create_board(self, cell_list):
        self.board = [cell_list[x:x+self.columns] for x in xrange(0, len(cell_list), self.columns)]

    def set_cell(self, position_tuple, player_name):
        cell = self.board[position_tuple[0]][position_tuple[1]]
        if cell.is_empty():
            cell.value = player_name

    def search_for_win(self, cell, direction):
        return self.count_sets_of_adjacent_checkers(cell, direction, 3) == 3

    def check_for_win(self, ):
        for cell in self:
            if not cell.is_empty():
                if (self.search_for_win(cell, "e") or
                    self.search_for_win(cell, "n") or
                    self.search_for_win(cell, "ne") or
                    self.search_for_win(cell, "se")):
                    return True
        return False

    def translate_direction_to_list(self, direction):
        tuple_list = [self.direction_tuples[direction] for direction in list(direction)]
        direction = [0, 0]
        for tup in tuple_list:
            direction[0] += tup[0]
            direction[1] += tup[1]
        return direction

    def get_connection(self, cell, direction, check_for_same=True,
                        row_change=0, col_change=0):
        if direction:
            dir_vals = self.translate_direction_to_list(direction)
            row_position = dir_vals[0] + cell.row
            column_position = dir_vals[1] + cell.col
        else:
            row_position = row_change + cell.row
            column_position = col_change + cell.col
        if (row_position >= 0 and column_position >= 0 and
            row_position < self.column_size and column_position < self.columns):
            if check_for_same:
                return (not cell.is_empty() and
                        cell.value == self.board[row_position][column_position].value)
            else:
                return (not self.board[row_position][column_position].is_empty()
                        and cell.is_empty())
        else:
            return None

    def count_sets_of_adjacent_checkers(self, cell, direction, max_count=4):
        counter = 0
        dir_vals = self.translate_direction_to_list(direction)
        while ( self.get_connection(cell, False, True, dir_vals[0], dir_vals[1])
                and counter <= max_count):
            cell = Cell(
                cell.value, cell.row + dir_vals[0], cell.col + dir_vals[1])
            counter += 1
        return counter

    def list_possible_moves(self, ):
        return [(cell.row, cell.col) for cell in self if cell.is_empty() and
                (self.get_connection(cell, "s", False) is None or
                 self.get_connection(cell, "s", False) is True)]



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
