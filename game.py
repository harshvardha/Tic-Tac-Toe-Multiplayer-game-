from serverPlayer import Player, Player2
class Game:
    def __init__(self, gameId: int):

        # gameId will be used to uniquely identify the game object
        self.gameId = gameId

        # player objects to store player names and signs('X' and 'Y')
        self.player1: Player
        self.player2: Player2

        # coordinates dictionary will store the sign at every coordinate
        self.coordinates = {}

        # newCoordinates will store the coordinates of the move made by the present allowed player
        self.newCoordinates: tuple

        # result variable will tell us in a boolean way that whether there is a winner or not
        self.result = False

        # resultCoordinates will store the list of tuples of coordinates through which the result is found
        self.resultCoordinates = []

        # This chance variable will be used to determine which sign will be displayed on the game board
        # if chance = True then player1 with sign 'X' is having the turn
        # if chance = False then player2 with sign 'O' is having the turn
        self.chance = True

        # ready will be used to know whether we have both the players ready to play the game
        self.ready = False

        # p1Went and p2Went will be used to know whether either of them is disconnected
        # if player1 get disconnected then p1Went will become True
        # if player2 get disconnected then p2Went will become True
        self.p1Went = False
        self.p2Went = False
    
    def addPlayer(self, playerNo, playerName):
        if(playerNo == 1):
            self.player1 = Player(playerName, "X", 1)
        elif(playerNo == 2):
            self.player2 = Player2(playerName, "O", 2, self.player1.getPlayerName())
            self.ready = True
    
    def playerStatus(self, playerNo: int):

        # This function will be used to check whether a particular player is disconnected or not
        # player1 will check for player2
        # and player2 will check for player1
        if(playerNo == 1):
            return self.p1Went
        elif(playerNo == 2):
            return self.p2Went
    
    def leaving(self, playerNo):

        # This function will be used by the players to update their status if they are leaving or getting disconnected
        if(playerNo == 1):
            self.p1Went = True
        elif(playerNo == 2):
            self.p2Went = True
        self.ready = False

    def addNewCoordinates(self, row: int, column: int):
        if(self.chance):
            self.coordinates[(row, column)] = self.player1.getSign()
        else:
            self.coordinates[(row, column)] = self.player2.getSign()
        self.newCoordinates = (row, column)
    
    def updateChance(self):
        # This function will decide whose chance it is to make a move
        if(self.chance):
            self.chance = False
        else:
            self.chance = True

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
    
    def getGameId(self) -> int:
        return self.gameId
    
    def getNewCoordinates(self):
        return self.newCoordinates
    
    def getChance(self):
        return self.chance

    def isReady(self) -> bool:
        return self.ready
    
    def getSign(self, playerNo):
        if(playerNo == 1):
            return self.player1.getSign()
        elif(playerNo == 2):
            return self.player2.getSign()
    
    def getPlayerName(self, playerNo):
        if(playerNo == 1):
            return self.player1.getPlayerName()
        elif(playerNo == 2):
            return self.player2.getPlayerName()
    
    def getPlayerObject(self, playerNo):
        if(playerNo == 1):
            return self.player1
        elif(playerNo == 2):
            return self.player2