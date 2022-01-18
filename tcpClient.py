import socket
import pickle

class Network:
    
    # The object of this class will be used to send data to server and recieve data from server
    # we will use the UDP protocol to send data to the server because it is better to use UDP for realtime multiplayer game
    def __init__(self):
        self.serverAddress = ("127.0.0.1", 5000)
        self.socketObject = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketObject.connect(self.serverAddress)
        self.sentMessage = ""
        self.recievedMessage = ""
    
    def sendDataToServer(self, data):

        # This function will be used to send data to the server whenever needed
        try:
            # Now serializing the data object
            self.sentMessage = pickle.dumps(data)

            # Now sending the data
            self.socketObject.send(self.sentMessage)
        except socket.error as e:
            print(e)
    
    def recvDataFromServer(self):

        # This function will be used to receive data from the server whenever needed
        try:
            # Now recieving the data
            data = self.socketObject.recv(2048)

            # Now deserializing the data
            self.recievedMessage = pickle.loads(data)
            return self.recievedMessage
        except socket.error as e:
            print(e)
    
    def closeConnection(self):
        self.socketObject.close()