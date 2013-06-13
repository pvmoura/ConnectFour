#!/usr/bin/env python

#Connect 4 for Python

class ConnectFour(object):
    def __init__(self, columns=7, column_size=6):
        self.board = Board(columns, column_size)

    def checkWinner(self):
        return self.board.checkHorizontal() or self.board.checkVerticalDiagonal()

    def checkValidInput(self, userInput):
        valid = False
        try:
            userInput = int(userInput)
        except ValueError:
            pass
        else:
            if userInput in range(1, self.board.columns + 1):
                valid = True
        if type(userInput) is str and userInput.lower() == 'q':
            valid = True
        return valid

    def play(self):
        player = 'P'
        while True:
            self.board.drawBoard()
            msg = player + '\'s turn. '
            d = raw_input(msg + "Enter a column number to move: ")
            if self.checkValidInput(d):
                try:
                    d = int(d)
                except ValueError:
                    pass
                if type(d) is int:
                    for index, row in enumerate(self.board.board):
                        if self.board.checkEmpty(index, d-1):
                            self.board.board[index][d-1] = player
                            if player == 'P':
                                player = 'C'
                            else:
                                player = 'P'
                            break
                else:
                    if d.lower() == 'q':
                        break
            potentialWinner = self.checkWinner()
            if potentialWinner:
               print str(potentialWinner) + " won the game!"
               self.board.drawBoard()
               break

class Board(object):
    def __init__(self, columns = 7, column_size = 6):
        self.columns = columns
        self.column_size = column_size
        self.board = []
        for i in range(self.column_size):
            r = []
            for j in range(self.columns):
                r.append('_')
            self.board.append(r)

    def checkEmpty(self, x, y):
        return self.board[x][y] == '_'

    def drawBoard(self):
        columnNumbers = ""
        for i in range(self.columns + 1):
            if i != 0:
                columnNumbers += str(i) + " "
        print "\n" + columnNumbers + "\n"
        for row in reversed(self.board):
            rowString = ""
            for elem in row:
                rowString += str(elem) + " "
            print rowString
        print ""

    def checkHorizontal(self):
        for row in self.board:
            pw = None
            print row
            if row.count('C') >= 4:
                pw = 'C'
            elif row.count('P') >= 4:
                pw = 'P'
            if pw:
                winCounter = 1
                prev_index = 0
                for index, val in enumerate(row):
                    if val == pw:
                        if prev_index + 1 == index:
                            winCounter += 1
                        prev_index = index
                print winCounter
                if winCounter == 4:
                    return pw
        return False

    def checkVerticalDiagonal(self):
        for rowIndex, row in enumerate(self.board):
            maxLength = len(self.board) - 4
            if rowIndex <= maxLength:
                for index, val in enumerate(row):
                    if val == 'C' or val == 'P':
                        # check vertical
                        if val == self.board[rowIndex + 1][index] and val == self.board[rowIndex + 2][index] and val == self.board[rowIndex + 3][index]:
                            return val
                        # check diagonal
                        if (index <= maxLength and val == self.board[rowIndex + 1][index + 1] and val == self.board[rowIndex + 2][index + 2] and val == self.board[rowIndex + 3][index + 3]) or \
                        (index >= maxLength and val == self.board[rowIndex + 1][index - 1] and val == self.board[rowIndex + 2][index - 2] and val == self.board[rowIndex + 3][index - 3]):
                            return val
        return False

if __name__ == '__main__':
    game = ConnectFour()
    game.play()
