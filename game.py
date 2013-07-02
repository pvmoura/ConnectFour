#!/usr/bin/env python

from board import Easy_Board, Hard_Board, Board
import sys
from players import HumanPlayer, ComputerPlayer


class ConnectFour(object):
    def __init__(self, cell_list=None, columns=7, column_size=6, human=False, level='easy'):
        self.adversaries = [HumanPlayer(), HumanPlayer(False, 'Q')]
        if not human:
            self.adversaries[1] = ComputerPlayer(level)
        if level == 'easy':
            self.board = Easy_Board()
        elif level == 'hard':
            self.board = Hard_Board()
        else:
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

    def play(self, ):
        self.current_player = self.adversaries[0]
        while not self.board.check_for_win():
            print self.board 
            move = self.read_player_move()
            if move in ('q', 'Q'):
                sys.exit(0)
            self.board.set_cell(move, self.current_player.name)
            self.current_player = self.get_next_player()[0]

        print self.board
        self.current_player = self.get_next_player()[0]
        print self.current_player.name, "won the game!"

    def get_next_player(self, ):
        for player in self.adversaries:
            player.turn = not player.turn
        return [player for player in self.adversaries if player.turn is True]

if __name__ == '__main__':
    game = ConnectFour()
    game.play()