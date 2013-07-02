#!/usr/bin/env python

class Board(object):
    def __init__(self, cell_list=None, columns=7, column_size=6):
        self.columns = columns
        self.column_size = column_size
        self.initialize_board()
        self.direction_tuples = {
            "n": (1, 0),
            "e": (0, 1),
            "s": (-1, 0),
            "w": (0, -1)
        }
        self.combination_directions = [('nw','se'), ('sw', 'ne'), ('w', 'e')]

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

    def get_cell(self, position_tuple):
        try:
            return self.board[position_tuple[0]][position_tuple[1]]
        except IndexError:
            return False


    def get_cell_by_change(self, cell, direction, multiplier=1):
        if type(direction) is str:
            change_list = self.translate_direction_to_list(direction)
        else:
            change_list = direction
        if multiplier > 1:
            change_list = [elem * multiplier for elem in change_list]
        row_change = cell.row + change_list[0]
        col_change = cell.col + change_list[1]
        if row_change < 0 or col_change < 0:
            return False
        return self.get_cell((row_change, col_change))

    def set_cell(self, position_tuple, player_name, overwrite=False):
        try:
            cell = self.board[position_tuple[0]][position_tuple[1]]
            if cell.is_empty() or overwrite:
                cell.value = player_name
        except IndexError:
            return False

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

    def translate_direction_to_opposite(self, direction):
        dir_list = self.translate_direction_to_list(direction)
        return [elem * -1 for elem in dir_list]


    def get_connection(self, cell, direction, check_for_same=True,
                        row_change=0, col_change=0, check_val=None):
        if direction:
            dir_vals = self.translate_direction_to_list(direction)
            row_position = dir_vals[0] + cell.row
            column_position = dir_vals[1] + cell.col
        else:
            row_position = row_change + cell.row
            column_position = col_change + cell.col
        value = cell.value
        if check_val:
            value = check_val
        if (row_position >= 0 and column_position >= 0 and
            row_position < self.column_size and column_position < self.columns):
            check_cell = self.get_cell((row_position, column_position))
            if check_for_same:
                return value == check_cell.value
            elif check_val:
                return (value == self.check_cell.value or check_cell.is_empty())
            else:
                return (not self.board[row_position][column_position].is_empty()
                        and cell.is_empty())
        else:
            return None

    def count_sets_of_adjacent_checkers(self, cell, direction, max_count=4,
                                        check_val=None, check_for_same=True):
        counter = 0
        if type(direction) is str:
            dir_vals = self.translate_direction_to_list(direction)
        else:
            dir_vals = direction
        while ( self.get_connection(cell, False, check_for_same, dir_vals[0], dir_vals[1], check_val)
                and counter <= max_count):
            cell = Cell(
                cell.value, cell.row + dir_vals[0], cell.col + dir_vals[1])
            counter += 1
        return counter

    def get_move_values(self, cell):
        # Here I want to return a dictionary with all the relevant information
        # that I'll need in my evaluate utility function
        # for example if the relevant square has possibilities on both endpoints
        # and if it is a win possibility
        # and then defensive information as well of course
        # pdb.set_trace()
        data = {}
        possible_wins = 0
        right_openings = 0
        #self.combination_directions = [('w', 'e')]
        for comb_direction in self.combination_directions:
            data[comb_direction] = {
                'pos_win': False
            }
            #left = self.check_for_holes(cell, comb_direction[0])
            left = self.get_empties(cell, comb_direction[0])
            right = self.get_empties(cell, comb_direction[1])
            left_endpoint = cell
            right_endpoint = cell
            # check if there are empties b4 changing endpoints
            left_holes = 0
            right_holes = 0
            chain = 0
            while left > 0: 
                left_holes += left
                pot_start = self.get_cell_by_change(left_endpoint, comb_direction[0], left + 1)
                if pot_start and pot_start.value == cell.value:
                    # pdb.set_trace()
                    chain += 1
                    # then these empties are holes.
                    #   left = self.get_empties(pot_start, comb_direction[0])
                    check_left = self.check_for_holes(pot_start, comb_direction[0])
                    left_endpoint = pot_start
                    if check_left:
                        if len(check_left) > 1:
                            left_endpoint = check_left[1]
                            left_holes += check_left[0]
                        else:
                            left = check_left[0]
                        left = self.get_empties(left_endpoint, comb_direction[0])
                    else:
                        left = 0
                else:
                    left_holes -= left
                    left = 0
            while right > 0:
                right_holes += right
                pot_right = self.get_cell_by_change(right_endpoint, comb_direction[1], right + 1)
                if pot_right and pot_right.value == cell.value:
                    chain += 1
                    check_right = self.check_for_holes(pot_right, comb_direction[1])
                    if check_right:
                        if len(check_right) > 1:
                            right_endpoint = check_right[1]
                            right_holes += check_right[0]
                        else:
                            right_endpoint = pot_right
                            right = check_right[0]
                    else:
                        right = 0
                else:
                    right_holes -= right
                    right = 0
            left_side = self.get_chain_and_empties(left_endpoint, comb_direction[0])
            right_side = self.get_chain_and_empties(right_endpoint, comb_direction[1])
            data[comb_direction]['left_holes'] = left_holes
            data[comb_direction]['right_holes'] = right_holes
            data[comb_direction]['left_openings'] = left_side[0]
            data[comb_direction]['right_openings'] = right_side[0]
            data[comb_direction]['chain_length'] = left_side[1] + right_side[1] + chain
            total_possible_chain = (left_side[0] + left_holes + right_side[0] +
                                    right_holes + left_side[1] + right_side[1])
            if total_possible_chain >= 3:
                possible_wins += 1
                data[comb_direction]['pos_win'] = True
        return data

    def find_possible_wins(self, cell, combination_direction):
        left_openings = self.get_chain_and_empties(cell, combination_direction[0])
        right_openings = self.get_chain_and_empties(cell, combination_direction[1])
        return (left_openings[0] + left_openings[1] + right_openings[0] + right_openings[1]) >= 3

    def check_for_holes(self, cell, direction):
        adjacent_empties = self.get_empties(cell, direction)
        if adjacent_empties > 0:
            endpoint = self.get_cell_by_change(cell, direction, adjacent_empties)
            if endpoint and endpoint.value == cell.value:
                original_val = endpoint.value
                connections = 1
                while (self.count_sets_of_adjacent_checkers(endpoint, dir_list) > 1 or
                       self.get_empties(endpoint, direction) > 0):
                    new_connections = self.count_sets_of_adjacent_checkers(endpoint, dir_list)
                    if endpoint.is_empty():
                        adjacent_empties += new_connections
                    else:
                        connections += new_connections
                    endpoint = self.get_cell_by_change(endpoint, direction)
                if endpoint.is_empty():
                    dir_list = self.translate_direction_to_opposite(direction)
                    backup = self.count_sets_of_adjacent_checkers(endpoint, dir_list)
                    adjacent_empties -= backup
                    endpoint = self.get_cell_by_change(endpoint, dir_list, backup)
                return (adjacent_empties, endpoint, connections)
            else:
                return (adjacent_empties, )
        else:
            return False

    def get_chain_and_empties(self, cell, direction):
        total_chain = self.count_sets_of_adjacent_checkers(cell, direction)
        endpoint = self.get_cell_by_change(cell, direction, total_chain)
        empties = 0
        if endpoint:
            empties = self.get_empties(cell, direction)
        return empties, total_chain

    def get_empties(self, cell, direction):
        empties = self.count_sets_of_adjacent_checkers(cell, direction, 6, '_')
        if cell.is_empty():
            empties += 1
        return empties

    def count_one_adjacent(self, cell, direction):
        return self.count_sets_of_adjacent_checkers(cell, direction, 1) == 1

    def count_two_adjacent(self, cell, direction):
        return self.count_sets_of_adjacent_checkers(cell, direction, 2) == 2

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
        self.center_weight = (self.distance_from_col_edge(column_terminal) +
                              self.distance_from_row_edge(row_terminal)) * .1
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