#!/usr/bin/env python

from board import Board
import sys
from players import HumanPlayer, ComputerPlayer


class ConnectFour(object):
    def __init__(self, cell_list=None, columns=7, column_size=6, human=False, level='hard'):
        self.adversaries = [HumanPlayer(), HumanPlayer(False, 'O')]
        if not human:
            self.adversaries[1] = ComputerPlayer(level=level)
        self.board = Board()

    def read_player_move(self, ):
        return self.current_player.move(self.board)

    def play(self, ):
        self.current_player = [player for player in self.adversaries
                               if player.turn is True][0]
        while True:
            print self.board
            move = self.read_player_move()
            if move in ('q', 'Q'):
                sys.exit(0)
            self.board.set_cell(move, self.current_player.name)
            over = self.board.game_over()
            if over:
                break
            self.current_player = self.get_next_player()[0]
            
        print self.board
        print "Cat's Game!" if over == 'tie' else \
              self.current_player.name + " won the game!"
        
    def get_next_player(self, ):
        for player in self.adversaries:
            player.turn = not player.turn
        return [player for player in self.adversaries if player.turn is True]

if __name__ == '__main__':
    game = ConnectFour()
    game.play()