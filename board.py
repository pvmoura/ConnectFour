#!/usr/bin/env python

import pdb

class Board(object):
    def __init__(self, columns=7, rows=6):
        self.columns = columns
        self.rows = rows
        self.initialize_board()
        self.direction_tuples = {
            "n": (1, 0),
            "e": (0, 1),
            "s": (-1, 0),
            "w": (0, -1),
            "nw": (1, -1),
            "ne": (1, 1),
            "se": (-1, 1),
            "sw": (-1, -1)
        }
        self.combination_directions = [('nw','se'), ('sw', 'ne'), ('w', 'e')]
        self.directions = ['n', 'e', 's', 'w', 'ne', 'se', 'nw', 'sw']
        self.possible_fours = []
        for cell in self:
            if cell.row <= rows - 4:
                for direction in self.directions:
                    new_cell = self.get_cell_by_change(cell, direction, 4)
                    if new_cell:
                        self.possible_fours.append(
                            (cell.get_address(), new_cell.get_address())
                        )


    def __iter__(self, ):
        """ Iterates through board list, yielding inner contents
        """
        for row in self.board:
            for col in row:
                yield col

    def __str__(self, ):
        """ Pretty print the board
        """
        def colorize(char):
            """ Colorize letters
            """
            char = str(char)
            if char == '_':
                char = '\033[30m' + char + '\033[0m'
            elif char == 'X':
                char = '\033[1;35m' + char + '\033[0m'
            elif char == 'O':
                char = '\033[1;34m' + char + '\033[0m'
            return char

        return ("\n" + '\033[92m' +
                " ".join([str(i) for i in range(1, self.columns + 1)]) +
                "\033[0m\n" +
                "\n".join(' '.join(map(colorize, row))
                    for row in reversed(self.board)) +
                "\n")

    def initialize_board(self, place_holder='_'):
        """ Initializes list of cell lists for board representation
        """
        self.board = [[ Cell('_', i, j, self.columns - 1, self.rows - 1)
                for j in range(self.columns)]
                for i in range(self.rows)]

    def get_cell(self, position_tuple):
        """ Get a cell object from board based on a position tuple
        """
        try:
            return self.board[position_tuple[0]][position_tuple[1]]
        except IndexError:
            return None

    def get_cell_by_change(self, cell, direction, multiplier=1):
        """ Get a cell object from the board going in a specific direction
            and a certain number of cells away
        """
        direction = self.direction_tuples[direction]
        if multiplier > 1:
            direction = [elem * multiplier for elem in direction]
        row_change = cell.row + direction[0]
        col_change = cell.col + direction[1]
        if row_change < 0 or col_change < 0:
            return None
        return self.get_cell((row_change, col_change))

    def set_cell(self, position_tuple, value, overwrite=False):
        """ Set a cell value with player_name at position_tuple
            Only writes to empty cells, unless overwrite=True
        """
        try:
            cell = self.board[position_tuple[0]][position_tuple[1]]
            if cell.is_empty() or overwrite:
                cell.set_val(value)
        except IndexError:
            return False

    def set_cell_to_empty(self, pos_tuple):
        self.set_cell(pos_tuple, '_', True)

    def search_for_win(self, cell, direction):
        """ Counts if there are 3 adjacent checkers in a row
            plus the given cell makes a win in specified direction
        """
        return self.count_chains_by_cell_val(cell, direction, 3) == 3

    def game_over(self, ):
        """ Calls search_for_win in all possible win directions
        """
        result = 'tie'
        for cell in self:
            if not cell.is_empty():
                if (self.search_for_win(cell, "e") or
                    self.search_for_win(cell, "n") or
                    self.search_for_win(cell, "ne") or
                    self.search_for_win(cell, "se")):
                    return True
            else:
                result = False
        return result

    def translate_direction_to_opposite(self, direction):
        """ Takes a direction string and translates to opposite values
            based on self.direction_tuples
        """
        return [elem * -1 for elem in self.direction_tuples[direction]]

    def check_adjacent_cell_value(self, cell, direction, check_for_nonempty=False):
        """ Checks if adjacent cell value is the same as a given cell's
            or if the given cell is empty this will check for nonempties
            in the given direction 
        """
        new_cell = self.get_cell_by_change(cell, direction)
        return (new_cell and ((not cell.is_empty() and new_cell.value == cell.value) or
               (check_for_nonempty and cell.is_empty() and not new_cell.is_empty())))

    def check_for_specific_val(self, cell, direction, check_val=None):
        """ Check if there is a specific value in a given direction from
            a given cell
        """
        new_cell = self.get_cell_by_change(cell, direction)
        return new_cell and check_val == new_cell.value

    def count_chains_by_cell_val(self, cell, direction, max_count=4,
                                 check_val=None, check_for_nonempty=False):
        """ Counts chains of checkers in a specific direction
        """
        counter = 0
        while (self.check_adjacent_cell_value(cell, direction,
                                              check_for_nonempty)
               and counter <= max_count):
            cell = self.get_cell_by_change(cell, direction)
            counter += 1
        return counter

    def count_chains_by_val(self, cell, direction, val=None):
        counter = 0
        while (self.check_for_specific_val(cell, direction, val)):
            cell = self.get_cell_by_change(cell, direction)
            counter += 1
        return counter

    def list_possible_moves(self, ):
        return [(cell.row, cell.col) for cell in self if cell.is_empty() and
                (self.get_cell_by_change(cell, "s", 1) is None or
                 self.check_adjacent_cell_value(cell, "s", True) is True)]

    def get_chain_holes_openings(self, cell, direction, holes=0, chain=0,
                                 openings=0):
        """ Take a cell and direction and output the number of holes, the length
            of the chain and the number of openings at the end of the chain
        """
        empties = self.get_empties(cell, direction)
        if not empties:
            if self.check_for_specific_val(cell, direction, cell.value):
                chain_len = self.count_chains_by_cell_val(cell, direction)
                chain += chain_len
                new_cell = self.get_cell_by_change(cell, direction, chain_len)
                if new_cell:
                    chain, holes, openings = self.get_chain_holes_openings(
                        new_cell, direction, holes, chain, openings)
            return chain, holes, openings
        else:
            new_cell = self.get_cell_by_change(cell, direction, empties + 1)
            if new_cell and new_cell.value == cell.value:
                chain += 1
                holes += empties
                chain, holes, openings = self.get_chain_holes_openings(
                    new_cell, direction, holes, chain, openings)
            else:
                openings += empties
            return chain, holes, openings

    def get_empties(self, cell, direction):
        """ Finds number of empty cells in a given direction from a given cell
        """
        if cell:
            empties = self.count_chains_by_val(cell, direction, '_')
            if cell.is_empty():
                empties += 1
            return empties
        return False

    def get_move_values(self, cell):
        # pdb.set_trace()
        data = {}
        for comb_direction in self.combination_directions:
            data[comb_direction] = {
                'pos_win': False,
                'both_sides_open': False
            }
            left_values = self.get_chain_holes_openings(cell, comb_direction[0])
            right_values = self.get_chain_holes_openings(cell, comb_direction[1])
            if left_values[2] > 0 and right_values[2] > 0:
                data[comb_direction]['both_sides_open'] = True
            data[comb_direction]['total_chain'] = left_values[0] + right_values[0]
            data[comb_direction]['total_holes'] = left_values[1] + right_values[1]
            data[comb_direction]['total_openings'] = left_values[2] + right_values[2]
            if sum(left_values) + sum(right_values) >= 3:
                data[comb_direction]['pos_win'] = True
        return data

    def count_one_adjacent(self, cell, direction):
        return self.count_chains_by_cell_val(cell, direction, 1) == 1

    def count_two_adjacent(self, cell, direction):
        return self.count_chains_by_cell_val(cell, direction, 2) == 2


class Cell(object):
    def __init__(self, value, row_index, column_index, row_terminal=6, column_terminal=5):
        self.value = value
        self.row = row_index
        self.col = column_index
        self.center_weight = (self.distance_from_col_edge(column_terminal) +
                              self.distance_from_row_edge(row_terminal))
        self.on_edge = self.is_edge(row_terminal, column_terminal)
        self.on_corner = self.is_corner(row_terminal, column_terminal)

    def __repr__(self, ):
        return "{value} at ({row}, {col})".format(value=self.value,
                                                  row=self.row,
                                                  col=self.col)
    def __str__(self, ):
        return self.value

    def set_val(self, val):
        self.value = val

    def get_address(self, ):
        return self.row, self.col

    def is_empty(self, ):
        return self.value == '_'

    def is_edge(self, row_terminal, column_terminal):
        return (self.row == 0 or self.row == row_terminal or
                self.col == 0 or self.col == column_terminal)

    def distance_from_col_edge(self, column_terminal):
        if self.col <= column_terminal/2:
            return self.col
        else:
            return column_terminal - self.col

    def distance_from_row_edge(self, row_terminal):
        if self.row < row_terminal/2:
            return self.row
        else:
            return row_terminal - self.row

    def is_corner(self, row_terminal, column_terminal):
        return ((self.row == 0 and self.col == 0) or
                (self.row == 0 and self.col == column_terminal) or
                (self.row == row_terminal and self.col == 0) or
                (self.row == row_terminal and self.col == column_terminal))