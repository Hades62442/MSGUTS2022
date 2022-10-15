import socket
import time
import random

import keyboard  # using module keyboard

msgFromClient = "requestjoin:simple"
name = "simple"

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

def main():
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
        
        print(msgFromServer)

        if "playerupdate" in msgFromServer:
            pos = msgFromServer.split(":")[1]
            posSplit = pos.split(",")
            posx = float(posSplit[0])
            posy = float(posSplit[1])
            if posSplit[-1].lower() == "true":
                gotten_key = True

        if "exit" in msgFromServer and gotten_key == True:
            x = msgFromServer.split(":")[1]
            x = x.split(",")
            targetPosX = int(posSplit[0])
            targetPosY = int(posSplit[1])

        elif "nearbyitem" in msgFromServer:
            x = msgFromServer.split(":")[1]
            x = x.split(",")
            for i, elt in enumerate(x):
                if elt == "redkey" and [int(x[i+1]), int(x[i+2])] not in visited_positions:
                    targetPosX = int(x[i+1])
                    targetPosY = int(x[i+2])
                    break
                elif elt == "treasure" and [int(x[i+1]), int(x[i+2])] not in visited_positions:
                    targetPosX = int(x[i+1])
                    targetPosY = int(x[i+2])
                    break

        elif "nearbyfloor" in msgFromServer:
            x = msgFromServer.split(":")[1]
            x = x.split(",")
            for i in range(len(x)//2):
                if [float(x[i]), float(x[i+1])] not in visited_positions:
                    targetPosX = float(posSplit[0])
                    targetPosY = float(posSplit[1])
        
        else:
            targetPosX = random.randint(0,500)
            targetPosY = random.randint(0,500)

        requestmovemessage = "moveto:" + str(targetPosX) + "," + str(targetPosY)
        SendMessage(requestmovemessage)
        visited_positions.append([targetPosX, targetPosY])


gotten_key = False
visited_positions = []
main()    