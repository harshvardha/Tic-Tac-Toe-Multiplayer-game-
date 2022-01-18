from player import Player1, Player2
class Model:
    def __init__(self):

        # player objects to store player names and signs('X' and 'Y')
        self.player1 = Player1()
        self.player2 = Player2()

        # coordinates dictionary will store the sign at every coordinate
        self.coordinates = {}

        # result variable will tell us in a boolean way that whether there is a winner or not
        self.result = False

        # resultCoordinates will store the list of tuples of coordinates through which the result is found
        self.resultCoordinates = []

        # This chance variable will be used to determine which sign will be displayed on the game board
        # if chance = True then player1 with sign 'X' is having the turn
        # if chance = False then player2 with sign 'O' is having the turn
        self.chance = True
    
    def createPlayers(self, player1Name, player2Name):
        self.player1.setPlayerName(player1Name)
        self.player2.setPlayerName(player2Name)
    
    def whoseChance(self, row: int, column: int):

        # This function will decide whose turn is now either player1 or player2
        # after deciding that it will return the respective sign
        if(self.chance):
            self.chance = False
            self.coordinates[(row, column)] = self.player1.getSign()
            return self.player1.getSign()
        self.chance = True
        self.coordinates[(row, column)] = self.player2.getSign()
        return self.player2.getSign()

    def checkResult(self, row: int, column: int):

        # This function will check for the win of one of the players after every move
        # with the help of the utility functions _checkRowWise, _checkColumnWise, checkLeftDiagonal, _checkRightDiagonal
        if(not self.result):
            self._checkRowWise(row)
            if(not self.result):
                self._checkColumnWise(column)
                if(not self.result):
                    if(row == column):
                        self._checkLeftDiagonal()
                        if(not self.result and (row == 1 and column == 1)):
                            self._checkRightDiagonal()
                    elif(row == 2 or column == 2):
                        self._checkRightDiagonal()
    
    def _checkRowWise(self, row: int):

        # This function will check for the result in the x direction of the give (row, column)
        column = 0
        try:
            while(self.coordinates[(row, column)] == self.coordinates[(row, column+1)]):
                column += 1
                self.result = True
                if(column == 2):
                    break
            else:
                self.result = False
        except KeyError:
            self.result = False
        if(self.result):
            for i in range(3):
                self.resultCoordinates.append((row, i))
            if(self.coordinates[(row, 0)] == "X"):
                self.resultCoordinates.append(self.player1.getPlayerName())
            elif(self.coordinates[(row, 0)] == "O"):
                self.resultCoordinates.append(self.player2.getPlayerName())
        

    def _checkColumnWise(self, column: int):
        
        # This function will check for the result in the y direction of the given (row, column)
        row = 0
        try:
            while(self.coordinates[(row, column)] == self.coordinates[(row+1, column)]):
                row += 1
                self.result = True
                if(row == 2):
                    break
            else:
                self.result = False
        except KeyError:
            self.result = False
        if(self.result):
            for i in range(3):
                self.resultCoordinates.append((i, column))
            if(self.coordinates[(0, column)] == "X"):
                self.resultCoordinates.append(self.player1.getPlayerName())
            elif(self.coordinates[(0, column)] == "O"):
                self.resultCoordinates.append(self.player2.getPlayerName())

    def _checkLeftDiagonal(self):
        
        # This function will check for the result in the left diagonal
        row = column = 0
        try:
            while(self.coordinates[(row, column)] == self.coordinates[(row+1, column+1)]):
                row += 1
                column += 1
                self.result = True
                if(row == 2 and column == 2):
                    break
            else:
                self.result = False
        except KeyError:
            self.result = False
        if(self.result):
            if(self.coordinates[(0, 0)] == "X"):
                self.resultCoordinates = [(0, 0), (1, 1), (2, 2), self.player1.getPlayerName()]
            elif(self.coordinates[(0,0)] == "O"):
                self.resultCoordinates = [(0, 0), (1, 1), (2, 2), self.player2.getPlayerName()]

    def _checkRightDiagonal(self):
        
        # This function will check for the result in the right diagonal
        row = 0
        column = 2
        try:
            while(self.coordinates[(row, column)] == self.coordinates[(row+1, column-1)]):
                row += 1
                column -= 1
                self.result = True
                if(row == 2 and column == 0):
                    break
            else:
                self.result = False
        except KeyError:
            self.result = False
        if(self.result):
            if(self.coordinates[(0, 2)] == "X"):
                self.resultCoordinates = [(0, 2), (1, 1), (2, 0), self.player1.getPlayerName()]
            elif(self.coordinates[(0, 2)] == "O"):
                self.resultCoordinates = [(0, 2), (1, 1), (2, 0), self.player2.getPlayerName()]
    
    def getResult(self):
        return self.result
    
    def getResultCoordinates(self):
        return tuple(self.resultCoordinates)
    
    def getNoOfCoordinatesAcquired(self):
        return len(self.coordinates)
    
    def reset(self):
        self.resultCoordinates.clear()
        self.coordinates.clear()
        self.player1.reset()
        self.player2.reset()
        self.chance = True
        self.result = False