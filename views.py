import tkinter

# frameProperties dictionary will contain the styling properties of the frame
frameProperties = {
    "bg" : "#ffffff"
}

class MessageBox(tkinter.Toplevel):
    def __init__(self, parent, winner, disconnected = False, **kwargs):
        super().__init__(master = parent, **kwargs)
        self.parent = parent
        self.winner = winner
        self.disconnected = disconnected
        if(not self.disconnected):
            self.title("Result")
        else:
            self.title("Alert")
        self.iconbitmap("tic-tac-toe.ico")
        self.geometry("%dx%d+%d+%d" % (400, 200, 550, 300))
        self.transient(parent)
        self.resizable(width = False, height = False)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel)
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self._createUI()
        self.focus_set()
        self.bind("<Escape>", self._cancel)
        self.bind("<Return>", self._cancel)
        self.wait_window()
    
    def _createUI(self):

        # labelProperties variable will contain the styling properties of the messageLabel
        labelProperties = {
            "bg" : "#FF8550",
            "fg" : "#FFFFFF",
            "font" : ("Showcard Gothic", 30),
            "wraplength" : 600
        }
        if(not self.disconnected):
            labelProperties["text"] = self.winner + "won"
        else:
            labelProperties["text"] = self.winner + " disconnected"
        messageLabel = tkinter.Label(master = self, **labelProperties)
        messageLabel.grid(row = 0, column = 0, sticky = (tkinter.N, tkinter.S, tkinter.E, tkinter.W))

        # buttonProperties variable will contain the styling properties of the ok button
        buttonProperties = {
            "bg" : "#FF8550",
            "fg" : "#000000",
            "bd" : 0,
            "activebackground" : "#FF8550",
            "text" : "ok",
            "font" : ("Showcard Gothic", 30),
            "command" : self._cancel
        }
        okButton = tkinter.Button(master = self, **buttonProperties)
        okButton.grid(row = 1, column = 0)
    
    def _cancel(self, event = None):
        self.withdraw()
        self.update_idletasks()
        self.parent.focus_set()
        self.destroy()

class BoardButton(tkinter.Button):
    def __init__(self, parent, row: int, column: int, **kwargs):
        super().__init__(master = parent, **kwargs)
        self.row = row
        self.column = column
    
    def getRow(self):
        return self.row
    
    def getColumn(self):
        return self.column

class MainWindow(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.configure(bg = "#FF8550")
        self.attributes("-fullscreen", True)
        self.iconbitmap("tic-tac-toe.ico")
        self.columnconfigure(0, weight = 1)
        #self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.exitButton = tkinter.Button(master = self, text = "exit", bd = 0, bg = "#FF8550", fg = "#000000", font = ("Showcard Gothic", 27),
            activebackground = "#FF8550", activeforeground = "#FFFFFF", command = lambda : self.destroy()
        )
        self.buttons = {}
        self.entryBoxes = {}
        self.labels = {}
        self.createPlayerInfoFrame()
    
    def createPlayerInfoFrame(self):

        # This function created the frame which will asks for he username of the two players who will play

        # Now creating the frames

        # creating the main container frame i.e information frame
        global frameProperties
        informationFrame = tkinter.Frame(master = self, **frameProperties)
        informationFrame.grid(column = 0, row = 1)
        informationFrame.columnconfigure(0, weight = 1)
        for i in range(3):
            informationFrame.rowconfigure(i, weight = 1)

        #frames dictionary will contain the actual frames which will contain the label and entry pair
        frames = {
            "player" : tkinter.Frame(master = informationFrame, **frameProperties)
        }

        # assembling the frames in the information frame using grid layout manager
        for i, value in enumerate(frames.values()):
            value.columnconfigure(0, weight = 1)
            for j in range(2):
                value.rowconfigure(j, weight = 1)
            value.grid(column = 0, row = i, padx = 20, pady = 20)

        # Now creating the labels and entry boxes for the information frame
        # labelProperties dictionary the styling information for the labels
        # labels dictionary contains the label widgets required
        labelProperties = {
            "bg" : "#ffffff",
            "fg" : "#000000",
            "font" : ("Showcard Gothic", 30)
        }
        self.labels = {
            "player" : tkinter.Label(master = frames["player"], text = "PLAYER USERNAME", **labelProperties),
            "waitingForOpponent" : tkinter.Label(master = self, text = "Waiting for opponent...", fg = "#FF8550",
            bg = "#FF8550", font = ("Showcard Gothic", 30))
        }

        # Now creating the entry boxes for the username input from the players
        # entryBoxProperties dictionary contains the styling information for the entry boxes
        # entryBox dictionary will contain the required entry widgets
        entryBoxProperties = {
            "bd" : 0,
            "bg" : "#FF8550",
            "font" : ("Showcard Gothic", 27),
            "fg" : "#ffffff",
        }
        self.entryBoxes = {
            "player" : tkinter.Entry(master = frames["player"], **entryBoxProperties)
        }

        # assembling the entry boxes and labels in the player1 and player2 frames respectively using grid layout manager
        for i, key in enumerate(self.entryBoxes.keys()):
            self.labels[key].grid(column = 0, row = i)
            self.entryBoxes[key].grid(column = 0, row = i+1)
        
        # buttonProperties dictionary will contain the styling properties of the button
        buttonProperties = {
            "bg" : "#FF8550",
            "fg" : "#ffffff",
            "bd" : 0,
            "font" : ("Showcard Gothic", 27),
            "text" : "START GAME",
            "activebackground" : "#FF8550",
            "activeforeground" : "#ffffff"
        }
        # buttons dictionary will contain the actual buttons required
        self.buttons = {
            "startGame" : tkinter.Button(master = informationFrame, **buttonProperties),
        }
        # assembling the buttons with grid layout manager
        self.buttons["startGame"].grid(column = 0, row = 2, pady = 20)
        self.exitButton.grid(column = 0, row = 0, sticky = (tkinter.N, tkinter.E, tkinter.S))
        self.labels["waitingForOpponent"].grid(row = 2, column = 0)
    
    def createGameBoard(self, player1Name, player2Name):

        # This function will first destroy the player info ui and then create the game board

        # destroying the player info ui
        for s in self.grid_slaves():
            if(type(s) == tkinter.Frame or type(s) == tkinter.Label):
                s.destroy()

        # Now we will confiure the weight of the row 0 and row 1
        # weight of row 0 will be 0
        # and weight of row 1 will be 1
        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)

        # Now started created the game board UI

        # Creating the frame which will the board
        global frameProperties
        boardFrame = tkinter.Frame(master = self, **frameProperties)
        boardFrame.grid(column = 0, row = 1, sticky = (tkinter.W, tkinter.E, tkinter.N, tkinter.S), padx = 200, pady = 20)
        for i in range(3):
            boardFrame.columnconfigure(i, weight = 1)
            boardFrame.rowconfigure(i, weight = 1)
        
        # Creating buttons for the board

        # buttonProperties dictionary will contain the styling prperties of the board buttons
        buttonProperties = {
            "bg" : "#FF8550",
            "bd" : 0,
            "fg" : "#000000",
            "activebackground" : "#FF8550",
            "font" : ("Showcard Gothic", 150)
        }

        # Creating buttons
        self.buttons = {
            "row1" : {}, "row2" : {}, "row3" : {}
        }

        # assembling the buttons and also creating the buttons
        for i, key in enumerate(self.buttons.keys()):
            for j in range(3):
                self.buttons[key]["button" + str(j)] = BoardButton(parent = boardFrame, row = i, column = j, **buttonProperties)
                self.buttons[key]["button" + str(j)].grid(column = j, row = i, sticky = (tkinter.N, tkinter.S, tkinter.W, tkinter.E))
                if(j % 2 != 0):
                    if(i % 2 == 0):
                        self.buttons[key]["button" + str(j)].grid_configure(padx = 20)
                    else:
                        self.buttons[key]["button" + str(j)].grid_configure(pady = 20, padx = 20)
                else:
                    if(i % 2 != 0):
                        self.buttons[key]["button" + str(j)].grid_configure(pady = 20)
        
        # Creating indicator labels of player username which will indicate the player whose chance is to play

        # creating the container frame for the indicator labels
        indicatorLabelContainer = tkinter.Frame(master = self, bg = "#FF8550")
        indicatorLabelContainer.columnconfigure(0, weight = 1)
        indicatorLabelContainer.columnconfigure(1, weight = 1)
        indicatorLabelContainer.grid(column = 0, row = 0, sticky = (tkinter.E, tkinter.W, tkinter.N, tkinter.S), padx = 20)

        # playerUsernameLabelProperties dictionary contains styling properties of usernames of "player1" and "player2"
        playerUsernameLabelProperties = {
            "font" : ("Showcard Gothic", 27),
            "bg" : "#FF8550"
        }
        # creating the labels dictionary
        self.labels = {}
        for i in range(2):
            self.labels["player" + str(i+1)] = tkinter.Label(master = indicatorLabelContainer, **playerUsernameLabelProperties)
            if(i == 0):
                self.labels["player1"].configure(fg = "#000000", text = player1Name)
                self.labels["player1"].grid(column = i, row = 0, sticky = (tkinter.W, tkinter.N, tkinter.S))
            elif(i == 1):
                self.labels["player2"].configure(fg = "#ffffff", text = player2Name)
                self.labels["player2"].grid(column = i, row = 0, sticky = (tkinter.E, tkinter.N, tkinter.S))
        self.exitButton.grid(row = 2, column = 0, sticky = tkinter.E)

    def getButtons(self):
        return self.buttons

    def getEntryBoxes(self):
        return self.entryBoxes
    
    def getButton(self, row, column):
        return self.buttons["row" + str(row + 1)]["button" + str(column)]
    
    def waitingForOpponent(self):
        self.labels["waitingForOpponent"].fg = "#000000"

    def updateGameBoard(self, sign, widget):
        if(widget.cget("text") == ""):
            if(sign == "X"):
                self.labels["player1"].configure(fg = "#ffffff")
                self.labels["player2"].configure(fg = "#000000")
            elif(sign == "O"):
                self.labels["player1"].configure(fg = "#000000")
                self.labels["player2"].configure(fg = "#ffffff")
            widget.configure(text = sign)
    
    def displayResult(self, resultCoordinates = [], disconnectionMessage = ""):
        # messageBoxProperties will contain the styling properties of message box that will pop up on the screen when there is a winner
        messageBoxProperties = {
            "bg" : "#FF8550"
        }
        if(disconnectionMessage == ""):
            for coordinate in resultCoordinates:
                if(type(coordinate) == tuple):
                    self.buttons["row" + str(coordinate[0]+1)]["button" + str(coordinate[1])].configure(bg = "#FFFFFF")
            if(len(resultCoordinates) == 4):
                MessageBox(self, resultCoordinates[3], **messageBoxProperties)
            else:
                MessageBox(self, "Its a tie", **messageBoxProperties)
        else:
            MessageBox(self, disconnectionMessage, True, **messageBoxProperties)
        slaveWidgets = self.grid_slaves()
        for widget in slaveWidgets:
            if(type(widget) == tkinter.Button and widget.cget("text") == "exit"):
                continue
            widget.destroy()
        self.rowconfigure(1, weight = 1)
        self.createPlayerInfoFrame()
    
    def updateTitle(self, title):
        self.title(title)