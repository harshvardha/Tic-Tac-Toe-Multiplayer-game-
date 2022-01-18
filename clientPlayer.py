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