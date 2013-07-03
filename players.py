#!/usr/bin/env python
"""
Connect 4 for Python
"""
import random
import copy
import pdb

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
    def __init__(self, turn=False, name='C',  opponent_name='P', current_board=None):
        self.name = name
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

    def move_mini(self, board):
        # what are the steps to get this to work?
        # 1. make a copy of the board. 2. move to the desired place. 3. check if you've reached a terminal state on board.
        # 4. if you have reached terminal call an evaluation function. 5. else keep recursing down 6. return a move
        def flip(player):
            return self.opponent if player == self.name else self.name

        def minimax_recurse(board, player, level=0, move=None):
            #pdb.set_trace()
            winner = board.check_for_win()
            moves = board.list_possible_moves()
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

    def move(self, board):
        return self.move_easy(board)

    def move_easy(self, board):
        possible_moves = board.list_possible_moves()
        pos_end = self.check_for_immediate_win(board, possible_moves)
        if pos_end:
            return pos_end
        evaluating_moves = []
        new_board = copy.deepcopy(board)
        for move in possible_moves:
            cell = new_board.get_cell(move)
            new_board.set_cell(move, self.name)
            player_data_dict = new_board.get_move_values(cell)
            player_utility = 0
            for key, val in player_data_dict.items():
                openings_multiplier = 1.5
                if val['both_sides_open']:
                    openings_multiplier = 2
                chain_multiplier = 3
                if val['total_holes'] > 0:
                    chain_multiplier = 2.5
                if val['total_chain'] == 2 and val['both_sides_open']:
                    player_utility += 10
                player_utility +=  val['total_openings'] * openings_multiplier + \
                            val['total_chain'] * chain_multiplier
            evaluating_moves.append((move, player_utility))
            new_board.set_cell(move, self.opponent, True)
            opponent_data_dict = new_board.get_move_values(cell)
            comp_utility = 0
            for key, val in opponent_data_dict.items():
                openings_multiplier = 1.5
                if val['both_sides_open']:
                    openings_multiplier = 2
                chain_multiplier = 3
                if val['total_holes'] > 0:
                    chain_multiplier = 2.5
                if val['total_chain'] == 2 and val['both_sides_open']:
                    comp_utility += 10
                comp_utility +=  val['total_openings'] * openings_multiplier + \
                            val['total_chain'] * chain_multiplier
            evaluating_moves.append((move, comp_utility))
            new_board.set_cell(move, '_', True)
        max_value = evaluating_moves.pop(evaluating_moves.index(max(evaluating_moves, key=lambda tup: tup[1])))
        new_board.set_cell(max_value[0], 'P')
        while (self.check_for_immediate_win(new_board, new_board.list_possible_moves())):
            print max_value[0]
            print evaluating_moves
            new_board.set_cell(max_value[0], '_')
            max_value = evaluating_moves.pop(evaluating_moves.index(max(evaluating_moves, key=lambda tup: tup[1])))
            new_board.set_cell(max_value[0], 'P')
        return max_value[0]

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
                checkers_in_a_row = (board.count_chains_by_cell_val(cell, direction[0]) +
                                     board.count_chains_by_cell_val(cell, direction[1]))
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
                if (board.count_chains_by_cell_val(cell, direction[0]) + 
                    board.count_chains_by_cell_val(cell, direction[1])) == check_value:
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

