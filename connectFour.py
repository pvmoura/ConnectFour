#!/usr/bin/env python
"""
Connect 4 for Python
"""
import sys
import random
import copy
import pdb

C_values = 0
P_values = 0

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

    def move_test(self, board):
        # add a move function for the computer
        self.current_board = board
        possible_moves = self.current_board.list_possible_moves()
        move = self.check_for_immediate_win(board, possible_moves)
        if move:
            return move
        return possible_moves[random.randint(0, len(possible_moves) - 1)][1] + 1

    def move(self, board):
        # what are the steps to get this to work?
        # 1. make a copy of the board. 2. move to the desired place. 3. check if you've reached a terminal state on board.
        # 4. if you have reached terminal call an evaluation function. 5. else keep recursing down 6. return a move
        def flip(player):
            return self.opponent if player == self.name else self.name

        def minimax_recurse(board, player, level=0, move=None):
            #pdb.set_trace()
            winner = board.check_for_win()
            moves = board.list_possible_moves()
            global C_values
            global P_values
            if player == self.name:
                C_values += 1
            else:
                P_values += 1
            if moves == [] or winner is not False or level > 3:
                return self.evaluate_board_utility(board, move), move
            else:
                new_board = copy.deepcopy(board)
                result_list = []
                for m in moves:
                    new_board.set_cell(m, player)
                    result_list.append(minimax_recurse(new_board, flip(player), level + 1, m))
                min_or_max = max if player == self.name else min
                result = min_or_max(result_list)
                return result[0], move if move is not None else result[1]
        pos_end = self.check_for_immediate_win(board, board.list_possible_moves())
        if pos_end:
            return pos_end
        return minimax_recurse(board, self.name, 0)[1]


    def evaluate_board_utility(self, board, move):
        # evaluate the current board position based on a set of heuristics, return a value
        #pdb.set_trace()
        winner = board.check_for_win()
        cell = board.get_cell(move)
        multiplier = 1
        if cell.value == self.opponent:
            multiplier = -1
        utility = 0
        if winner:
            utility += 100
        if move:
            
            for direction in board.combination_directions:
                # what do I want to do here? I would like to check if each move sets up a possible win
                # I want to count up the possible wins and apply some sort of weight to that value
                # I also want to take into account the possibility of doubling up. First thing is first.
                # Let's figure out how to count the possible wins
                # To count the possible wins, first count the number in a row. Then, check the endpoints for empty cells
                # Check both endpoints. A potential win in one direction weighs less than one in both directions
                checkers_in_a_row = (board.count_sets_of_adjacent_checkers(cell, direction[0]) +
                                     board.count_sets_of_adjacent_checkers(cell, direction[1]))
                board_data = board.get_move_values(cell)
                pos_wins = 0
                threes = 0
                twos = 0
                wide_opens = 0
                closed_ends = 0
                half_open = 0
                total_possibilities = 0
                for key, v in board_data.items():
                    if v['pos_win']:
                        pos_wins += 1
                    if v['chain_length'] >= 2:
                        threes += 1
                    elif v['chain_length'] > 0:
                        twos += 1
                    if v['right_openings'] > 0 and v['left_openings'] > 0:
                        wide_opens += 1
                    elif v['right_openings'] == 0 and v['left_openings'] == 0:
                        closed_ends += 1
                    else:
                        half_open += 1
                    total_possibilities += v['right_openings'] + v['left_openings'] + 5 * v['chain_length']

                utility += (pos_wins * 5 + threes * 2.5 + twos * 2 + total_possibilities * 3 + 
                           wide_opens * 2 + closed_ends * 0.5 + half_open)
                #utility += pos_wins
                utility += cell.center_weight * 100

            #print utility * multiplier
            return utility * multiplier

    def test_possible_moves(self, board, possible_moves, player_name,
                            direction_list, check_value):
        for move in possible_moves:
            cell = board.get_cell(move)
            for direction in direction_list:
                cell.value = player_name
                if (board.count_sets_of_adjacent_checkers(cell, direction[0]) + 
                    board.count_sets_of_adjacent_checkers(cell, direction[1])) == check_value:
                    cell.value = '_'
                    return move
                cell.value = '_'
        return False

    def check_for_immediate_win(self, board, possible_moves):
        combination_directions = [('nw','se'), ('ne', 'sw'), ('e', 'w'), ('s', 'n')]
        return_value = self.test_possible_moves(board, possible_moves,
                                            self.name, combination_directions, 3)
        if not return_value:
            return_value = self.test_possible_moves(board, possible_moves,
                                                self.opponent, combination_directions, 3)
        return return_value


class ConnectFour(object):
    def __init__(self, cell_list=None, columns=7, column_size=6):
        self.board = Board()

    def read_player_move(self, ):
        move = self.current_player.move(self.board)
        if type(move) is not tuple:
            try:
                move = int(move) - 1
                possible_moves = self.board.list_possible_moves()
                position = [elem for elem in possible_moves if elem[1] == move]
                move = position[0]
            except ValueError:
                pass
        return move

    def play(self, human=False):
        players = [HumanPlayer(), HumanPlayer(False, 'Q')]
        if not human:
            players[1] = ComputerPlayer()
        self.current_player = players[0]
        global C_values
        global P_values
        while not self.board.check_for_win():
            print self.board
            print C_values, P_values
            C_values = 0
            P_values = 0
            
            move = self.read_player_move()
            if move in ('q', 'Q'):
                sys.exit(0)
            self.board.set_cell(move, self.current_player.name)
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
            "e": (0, 1),
            "s": (-1, 0),
            "w": (0, -1)
        }
        self.directions = ['nw', 'ne', 'sw', 'se', 'e', 'w', 's']
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

    def create_board(self, cell_list):
        self.board = [cell_list[x:x+self.columns] for x in xrange(0, len(cell_list), self.columns)]

    def copy_board(self, ):
        cell_list = [Cell(cell.value, cell.row, cell.col) for cell in self]
        return Board(cell_list)

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

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
