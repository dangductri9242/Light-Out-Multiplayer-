#This is a TCP Server for the game

import socket
from _thread import *
import pickle
from game import GameIn
import sys

# Take the Ip address
args = sys.argv
server = args[1]
port = 5555

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#listening to the client
s.listen(2)
print("Waiting for a connection, Server Started")

#Initialize games
connected = set()
games = {}
idCount = 0

#Create a thread to iterate between players
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    game = games[gameId]

    #send the initial game
    conn.sendall(pickle.dumps(game))

    while True:
        try:
            data = conn.recv(8192 * 3).decode()
            # send information for the corresponding game
            if gameId in games:
                game = games[gameId]
                
                if not data:
                    #data had not sent
                    break
                else:
                    # if player send a move, update the move
                    if data != "get":
                        game.play(p, data)

                    #send the game with/without updates
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except: 
            break
    
    #Announcing lose connection
    print("Lost connection")

    #close game
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

#top level code
while True:

    #connect to the socket
    conn, addr = s.accept()
    print("Connected to:", addr)

    #creating multiple games
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = GameIn(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    #start new threads
    start_new_thread(threaded_client, (conn, p, gameId))
