from clientPlayer import Player

class Model:
    
    # This model class will help the client to send and recieve data to and from the server
    # This model class will use the object of network class to send and recieve data from the server
    # It will also be used to decide whether we can start the game or not based on the value of noOfplayers data member
    def __init__(self):
        # player object
        self.player: Player

        # chance variable will tell us whether we are allowed to make moves or not
        self.chance = True

        # ready variable will be used to know whether the model object is reset or not
        self.ready = False
    
    def createPlayer(self, playerObject):
        self.player = playerObject

    def whoseChance(self):
        return self.chance
    
    def getPlayerNo(self):
        return self.player.getPlayerNo()
    
    def getPlayerName(self):
        return self.player.getPlayerName()
    
    def updateChance(self, chance: bool):
        self.chance = chance

    def updateReady(self):
        if(not self.ready):
            self.ready = True
    
    def isReady(self):
        return self.ready
    
    def reset(self):
        del self.player
        self.chance = False
        self.ready = False
        self.playerNo = -1