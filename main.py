from views import MainWindow
from controller import Controller
from clientModel import Model
from tcpClient import Network
from coordinates import Coordinates

class Driver:
    def __init__(self):
        network = Network()
        if(network.recvDataFromServer() == "Connected"):
            Controller(MainWindow(), Model(), network, Coordinates())
        else:
            print("Not able to connect to server")

if __name__ == "__main__":
    Driver()