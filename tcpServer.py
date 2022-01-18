import socket
from threading import Thread
from game import Game
import pickle

host = ""
port = 5000
games = {}
playerCount = 0

def clientThread(clientSocket: socket.socket, clientAddress: tuple, playerNo: int, gameId: int):
    global games
    clientSocket.send(pickle.dumps("Connected"))
    reply = None
    print("games dictionary : ", games)
    print("game id : ", gameId)
    while(True):
        try:
            if(not games[gameId].isReady() and not games[gameId].playerStatus(2-playerNo+1)):
                data = pickle.loads(clientSocket.recv(1024))
                if(not data):
                    print("player " + str(playerNo) + " disconnected")
                    break
                print("Recieved data from player" + str(playerNo) + " : ",data)
                print("Player " + str(playerNo) + " : adding player\n")
                games[gameId].addPlayer(playerNo, data)
                reply = games[gameId].getPlayerObject(playerNo)
                clientSocket.sendall(pickle.dumps(reply))
                if(playerNo == 1):
                    while(not games[gameId].isReady()):
                        continue
                    reply = games[gameId].getPlayerName(2)
                    clientSocket.sendall(pickle.dumps(reply))
            else:
                if(games[gameId].playerStatus(2-playerNo+1)):
                    print("Player " + str(2-playerNo+1)+" disconnected")
                    clientSocket.sendall(pickle.dumps(games[gameId]))
                    del games[gameId]
                    break
                else:
                    print("Player " + str(playerNo) + " : game running")
                    if(playerNo == 1 and not games[gameId].getChance()):
                        while(games[gameId].isReady() and not games[gameId].getChance()):
                            continue
                        if(games[gameId].playerStatus(2-playerNo+1)):
                            print("Player " + str(playerNo) + " : Opponent disconnected")
                            clientSocket.sendall(pickle.dumps(games[gameId]))
                            del games[gameId]
                            break
                        elif(games[gameId].playerStatus(playerNo)):
                            break
                        print("sending to player 1 : ", games[gameId])
                        try:
                            clientSocket.sendall(pickle.dumps(games[gameId]))
                        except socket.error as e:
                            print("Player " + str(playerNo) + " : " + e)
                            print("Player " + str(playerNo) + " : disconnected")
                            break
                    elif(playerNo == 2):
                        while(games[gameId].isReady() and games[gameId].getChance()):
                            continue
                        if(games[gameId].playerStatus(2-playerNo+1)):
                            print("Player " + str(playerNo) + " : Opponent disconnected")
                            clientSocket.sendall(pickle.dumps(games[gameId]))
                            del games[gameId]
                            break
                        elif(games[gameId].playerStatus(playerNo)):
                            break
                        print("sending to player 2 : ", games[gameId])
                        try:
                            clientSocket.sendall(pickle.dumps(games[gameId]))
                        except socket.error as e:
                            print("Player " + str(playerNo) + " : " + e)
                            print("Player " + str(playerNo) + " : disconnected")
                            break
                    data = pickle.loads(clientSocket.recv(1024))
                    if(not data or games[gameId].playerStatus(2-playerNo+1)):
                        if(not data):
                            print("Player " + str(playerNo) + " : disconnected")
                        elif(games[gameId].playerStatus(2-playerNo+1)):
                            print("Player " + str(playerNo) + " : Opponent disconnected")
                            clientSocket.sendall(pickle.dumps(games[gameId]))
                            del games[gameId]
                        break
                    games[gameId].addNewCoordinates(data.getRowNo(), data.getColumnNo())
                    games[gameId].checkResult(data.getRowNo(), data.getColumnNo())
                    games[gameId].updateChance()
                    clientSocket.sendall(pickle.dumps(games[gameId]))
        except:
            break
    print("Connection closed with ", clientAddress)
    if(gameId in games):
        games[gameId].leaving(playerNo)
    clientSocket.close()
    
def main():
    global host, port, playerCount, games
    run = True
    acceptConnectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        acceptConnectionSocket.bind((host, port))
    except socket.error as e:
        print("Socket connection error",e)
    acceptConnectionSocket.listen()
    print("Server started, waiting for connections\n")
    while(run):
        clientInteractionSocket, clientAddress = acceptConnectionSocket.accept()
        print("IP address and port of client : %s, %s" % clientAddress)
        playerCount += 1
        playerNo = 0
        gameId = (playerCount - 1)//2
        if(playerCount % 2 == 1):
            print("Creating a new Game")
            games[gameId] = Game(gameId)
            playerNo = 1
        else:
            playerNo = 2
        t = Thread(target = clientThread, args = (clientInteractionSocket, clientAddress, playerNo, gameId))
        t.setDaemon(True)
        t.start()
main()