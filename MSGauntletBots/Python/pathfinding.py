# boilerplate
import socket
import time
import numpy as np
import random

msgFromClient = "requestjoin:dijkstra"
name = "dijkstra"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

directions = ["n","s","e","w","nw","sw","ne","se"]

# Create a UDP socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Send to server using created UDP socket
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def SendMessage(requestmovemessage):
    bytesToSend = str.encode(requestmovemessage)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)
    print("Sent message")

def update_map(map,playerPosX,playerPosY,msgFromServer):

    # generate floorX, floorY
    floorX = []
    floorY = []
    if "nearbyfloor" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        for i, item in enumerate(x):
            try:
                if i % 2 == 0:
                    floorX.append(int(item))
                else:
                    floorY.append(int(item))
            except ValueError:
                pass

    # generate itemsNearby
    itemsNearby = []
    if "nearbyitem" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        for i in range(round(len(x)/3)):
            itemsNearby.append([x[3*i], int(x[3*i+1]), int(x[3*i+2])])
            #itemsNearby[x[3*i]] = [int(x[3*i + 1]), int(x[3*i + 2])]

    # plot locations of floors (ie navigable space) on map 
    for i in range(len(floorX)):
            map[floorX[i]][floorY[i]] = 500

    for item in itemsNearby:
        # item: food V ammo V key V treasure
        map[item[1]][item[2]] = rewards[item[0]]

    print("Updated map")
    return map

def get_target(map,playerPosX,playerPosY):
    min_val = 1000
    target_node = [playerPosX,playerPosY]
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != 1000 and map[i][j] < min_val and i != 0:
                min_val = map[i][j]
                target_node = [i,j]

    print("Got target node")
    return target_node

def get_path(map, target_node):
    pass

actions = {0:"stop:", 1:"fire:", 2:"facedirection:n",3:"facedirection:nw",4:"facedirection:w",5:"facedirection:sw",6:"facedirection:s", 7:"facedirection:se",8:"facedirection:e",9:"facedirection:ne", 10:"movedirection:n", 11:"movedirection:nw",12:"movedirection:w",13:"movedirection:sw",14:"movedirection:s",15:"movedirection:se",16:"movedirection:e", 17:"movedirection:ne"} 
rewards = {"food":15, "ammo":10, "redkey":0, "yellowkey":1000, "bluekey":1000, "greenkey":1000, "treasure":5}        
map = [[None]*500]*500

for i in range(len(map)):
    for j in range(len(map[i])):
        map[i][j] = 1000

counter = 0

while True:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    print(msgFromServer)

    if "playerjoined" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        playerPosX = x[2]
        playerPosY = x[3]

    map = update_map(map, playerPosX, playerPosY, msgFromServer)
    #print(map)
    target_node = get_target(map,playerPosX,playerPosY)
    print(target_node)
    print(map[int(target_node[0])][int(target_node[1])])

    requestmovemessage = "moveto:" + str(target_node[0])  + "," + str(target_node[1])
    print(requestmovemessage)
    SendMessage(requestmovemessage)

    previousPosX = playerPosX
    previousPosY = playerPosX
    playerPosX = target_node[0]
    playerPosY = target_node[1]

    if previousPosX == playerPosX and previousPosY == playerPosY:
        counter += 1

    if counter >= 100:
        counter = 0
        requestmovemessage = "movedirection:" + random.choice([["n","s","e","w","nw","sw","ne","se"]])

    print(f"Counter: {counter}")

    #path = get_path(map, target_node)
    #move_along_path(path)