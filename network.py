#This class representing the network, act like the middle point between the server and the client.
import socket
import pickle

class Network:
    def __init__(self,IP):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # client socket
        self.server = IP # client IP 
        self.port = 5555 # client port number
        self.addr = (self.server, self.port)# client address
        self.p = self.connect() #connecting to client

    #get Player
    def getP(self):
        return self.p

    #connect to client
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(4096*8).decode()
        except:
            pass
    
    #send data to the server
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096*8))
        except socket.error as e:
            print(e)
