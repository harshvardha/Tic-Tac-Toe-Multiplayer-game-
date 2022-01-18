from threading import Thread

class Controller:
    def __init__(self, viewObject, modelObject, networkObject, coordinatesObject):
        self.viewObject = viewObject
        self.modelObject = modelObject
        self.networkObject = networkObject
        self.coordinatesObject = coordinatesObject
        self.threadObject = None
        self.gameObject = None
        self._registerPlayerInfoButtonEvents()
        self.viewObject.mainloop()
    
    def _registerPlayerInfoButtonEvents(self):
        buttons = self.viewObject.getButtons()
        buttons["startGame"].configure(command = self._collectPlayersInformation)
    
    def _collectPlayersInformation(self):
        entryBoxes = self.viewObject.getEntryBoxes()
        playerName = entryBoxes["player"].get()
        self.networkObject.sendDataToServer(playerName)
        print("sent : ", playerName)
        player = self.networkObject.recvDataFromServer()
        player.displayDetails()
        self.modelObject.createPlayer(player)
        if(self.modelObject.getPlayerNo() == 1):
            run = True
            self.viewObject.waitingForOpponent()
            while(run):
                player = self.networkObject.recvDataFromServer()
                if(player):
                    run = False
            self.modelObject.updateReady()
            self.viewObject.createGameBoard(self.modelObject.getPlayerName(), player)
            self.viewObject.updateTitle("Player 1")
        elif(self.modelObject.getPlayerNo() == 2):
            self.viewObject.createGameBoard(player.getPlayer1Name(), player.getPlayerName())
            self.modelObject.updateReady()
            self.viewObject.updateTitle("Player 2")
        self._registerGameBoardButtonEvents()
    
    def _registerGameBoardButtonEvents(self):
        buttons = self.viewObject.getButtons()
        bindingFunction = None
        if(self.modelObject.getPlayerNo() == 1):
            bindingFunction = self.updateFromPlayer1
        elif(self.modelObject.getPlayerNo() == 2):
            bindingFunction = self.updateFromPlayer2
        for key in buttons.keys():
            if(key != "restartButton"):
                for button in buttons[key].values():
                    button.bind("<Button-1>", bindingFunction)
            else:
                buttons[key].configure(command = self._restartGame)
        if(self.modelObject.getPlayerNo() == 2):
            self.threadObject = Thread(target = self.waitForOpponent)
            self.threadObject.setDaemon(True)
            self.threadObject.start()

    def updateFromPlayer1(self, event = None):
        if(self.modelObject.whoseChance()):
            self.updateGameBoard(event)
            if(self.modelObject.isReady() and self.modelObject.getPlayerNo() == 1 and not self.modelObject.whoseChance()):
                self.threadObject = Thread(target = self.waitForOpponent)
                self.threadObject.setDaemon(True)
                self.threadObject.start()

    def updateFromPlayer2(self, event = None):
        if(not self.modelObject.whoseChance()):
            self.updateGameBoard(event)
            if(self.modelObject.isReady() and self.modelObject.getPlayerNo() == 2 and self.modelObject.whoseChance()):
                self.threadObject = Thread(target = self.waitForOpponent)
                self.threadObject.setDaemon(True)
                self.threadObject.start()
        
    def updateGameBoard(self, event):
        if(event == None):
            if(self.gameObject.isReady()):
                self.modelObject.updateChance(self.gameObject.getChance())
                newCoordinates = self.gameObject.getNewCoordinates()
                button = self.viewObject.getButton(newCoordinates[0], newCoordinates[1])
                sign = self.gameObject.getSign(2 - self.modelObject.getPlayerNo() + 1)
                if(button.cget("text") == ""):
                    self.viewObject.updateGameBoard(sign, button)
                self.checkResult()
            else:
                self.displayDisconnectionMessage()
        else:
            row, column = event.widget.getRow(), event.widget.getColumn()
            self.coordinatesObject.setRowNo(row)
            self.coordinatesObject.setColumnNo(column)
            self.networkObject.sendDataToServer(self.coordinatesObject)
            self.gameObject = self.networkObject.recvDataFromServer()
            self.modelObject.updateChance(self.gameObject.getChance())
            if(self.gameObject.isReady()):
                sign = self.gameObject.getSign(self.modelObject.getPlayerNo())
                self.viewObject.updateGameBoard(sign, event.widget)
                self.checkResult()
            else:
                self.displayDisconnectionMessage()
    
    def checkResult(self):
        if(self.gameObject.getResult()):
            self.viewObject.displayResult(self.gameObject.getResultCoordinates())
            self.modelObject.reset()
            self._registerPlayerInfoButtonEvents()
        elif(self.gameObject.getNoOfCoordinatesAcquired() == 9):
            self.viewObject.displayResult()
            self.modelObject.reset()
            self._registerPlayerInfoButtonEvents()
    
    def displayDisconnectionMessage(self):
        playerName = self.gameObject.getPlayerName(2 - self.modelObject.getPlayerNo() + 1)
        self.viewObject.displayResult(disconnectionMessage = playerName)
        self.modelObject.reset()
        self._registerPlayerInfoButtonEvents()

    def waitForOpponent(self):
        print("waiting for opponent")
        self.gameObject = self.networkObject.recvDataFromServer()
        if(self.modelObject.getPlayerNo() == 1):
            self.updateFromPlayer2()
        elif(self.modelObject.getPlayerNo() == 2):
            self.updateFromPlayer1()
        print("thread ending")
    
    def _restartGame(self):
        self.viewObject.restartGame()
        self.modelObject.reset()