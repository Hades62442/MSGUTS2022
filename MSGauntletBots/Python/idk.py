import socket
import time
import random

import keyboard  # using module keyboard

msgFromClient = "requestjoin:idk"
name = "idk"

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

map = [["node"]*500]*500

class node:
    def __init__(self, cost, property):
        self.c = cost
        self.p = property

for elt in map:
    elt = node(10, None)

def main():
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