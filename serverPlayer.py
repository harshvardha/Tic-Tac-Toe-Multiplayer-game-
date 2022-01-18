class Player:
    def  __init__(self, playerName, sign, playerNo) -> None:
        self.name = playerName
        self.sign = sign
        self.playerNo = playerNo
    
    def getPlayerName(self):
        return self.name
    
    def getSign(self):
        return self.sign

    def getPlayerNo(self):
        return self.playerNo
    
    def displayDetails(self):
        print("Player Name : ", self.name)
        print("Player No : ", self.playerNo)
        print("Player Sign : ", self.sign)

class Player2(Player):
    def __init__(self, playerName, sign, playerNo, player1Name):
        super().__init__(playerName, sign, playerNo)
        self.player1Name = player1Name
    
    def getPlayer1Name(self):
        return self.player1Name