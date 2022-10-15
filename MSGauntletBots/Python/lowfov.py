# boilerplate
import socket
import time
import numpy as np
import random

msgFromClient = "requestjoin:fov"
name = "fov"

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

adjacent_map = [1000] * 8
while True:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    print(msgFromServer)

    if "playerjoined" in msgFromServer or "playerupdate" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        playerPosX = int(x[2])
        playerPosY = int(x[3])

    adjacent_nodes = []
    adjacent_nodes.append([playerPosX-1,playerPosY-1])
    adjacent_nodes.append([playerPosX-1,playerPosY])
    adjacent_nodes.append([playerPosX-1,playerPosY+1])
    adjacent_nodes.append([playerPosX,playerPosY-1])
    adjacent_nodes.append([playerPosX,playerPosY+1])
    adjacent_nodes.append([playerPosX+1,playerPosY-1])
    adjacent_nodes.append([playerPosX+1,playerPosY])
    adjacent_nodes.append([playerPosX+1,playerPosY+1])
    
    wall_nodes = []
    floor_nodes = []
    item_nodes = []

    if "nearbywall" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        for i in range(len(x)//2):
            x[i] = int(x[i])
            x[i+1] = int(x[i+1])
            wall_nodes.append([x[i], x[i+1]])

    if "nearbyfloor" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        for i in range(len(x)//2):
            x[i] = int(x[i])
            x[i+1] = int(x[i+1])
            floor_nodes.append([x[i], x[i+1]])

    if "nearbyitem" in msgFromServer:
        x = msgFromServer.split(":")[1]
        x = x.split(",")
        for i in range(len(x)//3):
            item_nodes.append([int(x[3*i+1]), int(x[3*i+2])])

    for i, node in enumerate(adjacent_nodes):
        if node in wall_nodes:
            adjacent_map[i] = 1000
        elif node in floor_nodes:
            adjacent_map[i] = 500
        elif node in item_nodes:
            adjacent_map[i] = 100

    min_val = min(adjacent_map)
    min_index = adjacent_map.index(min_val)
    requestmovemessage = "moveto:" + str(adjacent_nodes[min_index][0]) + "," + str(adjacent_nodes[min_index][1])
    SendMessage(requestmovemessage)

    print(adjacent_nodes)
    print(adjacent_map)