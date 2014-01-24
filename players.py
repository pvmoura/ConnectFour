#!/usr/bin/env python
"""
Connect 4 for Python
"""
import random
import copy
import pdb

class HumanPlayer(object):
    def __init__(self, turn=True, name='X'):
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
                try:
                    move = int(move) - 1
                    possible_moves = board.list_possible_moves()
                    position = [elem for elem in possible_moves if elem[1] == move]
                    move = position[0]
                except ValueError:
                    pass
                return move

class ComputerPlayer(object):
    def __init__(self, turn=False, name='O',  opponent_name='X',
                 current_board=None, level='easy'):
        self.name = name
        self.turn = turn
        self.opponent = opponent_name
        self.level = level
    
    def move(self, board):
        """ Computer move
        """
        possible_moves = board.list_possible_moves()
        pos_end = self.check_for_immediate_win(board, possible_moves)
        if pos_end:
            return pos_end
        make_move = self.move_mini if self.level == 'hard' else self.move_easy
        return make_move(board, possible_moves)

    def random_move(self, board, possible_moves):
        """ Generate a random move
        """
        # add a move function for the computer
        return possible_moves[random.randint(0, len(possible_moves) - 1)][1] + 1

    def test_for_win(self, board, possible_moves, name):
        """ Check if a possible move will end the game
        """
        for move in possible_moves:
            board.set_cell(move, name)
            if board.game_over() is True:
                board.set_cell_to_empty(move)
                return move
            board.set_cell_to_empty(move)
        return False

    def check_for_immediate_win(self, board, possible_moves):
        """ checks for immediate win
        """
        return_value = self.test_for_win(board, possible_moves, self.name)
        if not return_value:
            return_value = self.test_for_win(board, possible_moves, self.opponent)
        return return_value

    def move_mini(self, board, possible_moves):
        """ Penne, a little too al dente.
        """
        def flip(player):
            return self.opponent if player == self.name else self.name

        def minimax_recurse(board, player, level=0, move=None):
            #pdb.set_trace()
            winner = board.game_over()
            moves = board.list_possible_moves()
            if moves == [] or winner is not False or level > 4:
                multiplier = 1 if player == self.name else -1
                return self.evaluate_board_utility(board, move, winner, player) \
                       * multiplier, move
            else:
                new_board = copy.deepcopy(board)
                result_list = []
                for m in moves:
                    new_board.set_cell(m, player)
                    result_list.append(minimax_recurse(new_board, flip(player), level + 1, m))
                min_or_max = max if player == self.name else min
                result = min_or_max(result_list, key=lambda tup: tup[0])
                return result[0], move if move is not None else result[1]
        
        return minimax_recurse(board, self.name, 0)[1]

    def evaluate_board_utility(self, board, move, winner, player):
        """ 
        """
        if winner == 'tie':
            return 0
        elif winner == 'win':
            return 100000
        utility = 0
        for possible_four in board.possible_fours:
            move_utility = 0
            start = possible_four[0]
            cell = board.get_cell(start)
            if not cell.is_empty() and cell.value == player:
                data = board.get_move_values(cell)
                for key, val in data.iteritems():
                    if val['pos_win']:
                        move_utility += 100 + val['total_chain'] * 100
                        utility += move_utility
        return utility

    def move_easy(self, board, possible_moves):
        """ finds a move 
        """
        evaluating_moves = []
        new_board = copy.deepcopy(board)
        comp_move_utilities = self.return_naive_utility(
            new_board, possible_moves, self.name)
        opp_move_utilities = self.return_naive_utility(
            new_board, possible_moves, self.opponent)
        evaluating_moves = comp_move_utilities + opp_move_utilities
        max_value = evaluating_moves.pop(
            evaluating_moves.index(max(evaluating_moves, key=lambda tup: tup[1])))
        new_board.set_cell(max_value[0], self.name)
        while self.test_for_win(
            new_board, new_board.list_possible_moves(), self.opponent) is not False:
            if len(evaluating_moves) == 0:
                break
            new_board.set_cell_to_empty(max_value[0])
            max_value = evaluating_moves.pop(
                evaluating_moves.index(max(evaluating_moves, key=lambda tup: tup[1])))
            new_board.set_cell(max_value[0], self.opponent)
        return max_value[0]

    def return_naive_utility(self, board, possible_moves, player):
        """ returns a list of moves and utility
        """
        output_list = []
        for move in possible_moves:
            move_utility = 0
            cell = board.get_cell(move)
            board.set_cell(move, player)
            player_data_dict = board.get_move_values(cell)
            for key, val in player_data_dict.iteritems():
                openings_multiplier = 1.5
                if val['both_sides_open']:
                    openings_multiplier = 2
                chain_multiplier = 3
                if val['total_holes'] > 0:
                    chain_multiplier = 2.5
                if val['total_chain'] == 2 and val['both_sides_open']:
                    move_utility += 100
                move_utility +=  val['total_openings'] * openings_multiplier + \
                    val['total_chain'] * chain_multiplier + cell.center_weight
            output_list.append((move, move_utility))
            board.set_cell_to_empty(move)
        return output_list

