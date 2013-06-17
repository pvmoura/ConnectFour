#!/usr/bin/env python

from connectFour import Board

def checkWinners(board, addDistractions=False, vertical=False, gamePiece='P'):
    """ Generates vertical and horizontal winning boards and checks if the winner checkers work"""
    rangeValue = board.columns
    structure = "row"
    method = board.checkHorizontal
    if vertical:
        rangeValue = board.column_size
        structure = "column"
        method = board.checkVerticalDiagonal
    for i in range(rangeValue - 1):
        print "Now checking " + structure + ": " + str(i)
        offset = 0
        while offset <= rangeValue - 4:
            for j in range(offset, offset + 4):
                if not vertical:
                    board.board[i][j] = gamePiece
                else:
                    board.board[j][i] = gamePiece
            if not method():
                print errorMessage(i, offset, board.board[i], structure)
            if addDistractions:
                if not vertical:
                    board.board[i][offset - 2] = gamePiece
                else:
                    board.board[offset - 2][i] = gamePiece
                if not method():
                    print errorMessage(i, offset, board.board[i], structure)
                if offset == 0:
                    if not vertical:
                        board.board[i][offset - 1] = gamePiece
                    else:
                        board.board[offset - 1][i] = gamePiece
                elif offset == board.columns - 4:
                    if not vertical:
                        board.board[i][offset - 3] = gamePiece
                    else:
                        board.board[offset - 3][i] = gamePiece
                if not method():
                    print errorMessage(i, offset, board.board[i], structure)
            board.resetBoard()
            offset += 1

def errorMessage(row, offset, other, structure):
    return "Didn't work for " + structure + " " + str(row) + " and offset: " + str(offset) + " looking like: " + str(other)

def checkDiagonals(board, gamePiece='P', addDistractions=False):
    """Generates diagonal winning boards and checks if winning checkers work"""
    for i in range(board.column_size - 1):
        
        print "Now checking column: " + str(i)
        offset = 0
        #while offset <= board.column_size - 4:
            #for j in range(offset, offset + 4):
                #board.board

if __name__ == '__main__':
    b = Board()
    checkWinners(b, True)
    checkWinners(b, True, True)