import socket
import time
import random

import keyboard  # using module keyboard

msgFromClient = "requestjoin:habakuk"
name = "habakuk"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

#bunch of timers and intervals for executing some sample commands
moveInterval = 10
timeSinceMove = time.time()

fireInterval = 5
timeSinceFire = time.time()

stopInterval = 30
timeSinceStop = time.time()

directionMoveInterval = 15
timeSinceDirectionMove = time.time()

directionFaceInterval = 9
timeSinceDirectionFace = time.time()

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
        
        ##uncomment to see message format from server
        print(msgFromServer)

        if "playerupdate" in msgFromServer:
            pos = msgFromServer.split(":")[1]
            posSplit = pos.split(",")
            posx = float(posSplit[0])
            posy = float(posSplit[1])

        if keyboard.is_pressed('a'): # move left
            requestmovemessage = "moveto:" + str(posx - 10)  + "," + str(posy)
            SendMessage(requestmovemessage)
            print(requestmovemessage)

        if keyboard.is_pressed('s'): # move down
            requestmovemessage = "moveto:" + str(posx)  + "," + str(posy + 10)
            SendMessage(requestmovemessage)
            print(requestmovemessage)

        if keyboard.is_pressed('d'): # move right
            requestmovemessage = "moveto:" + str(posx + 10)  + "," + str(posy)
            SendMessage(requestmovemessage)
            print(requestmovemessage)

        if keyboard.is_pressed('w'): # move up
            requestmovemessage = "moveto:" + str(posx)  + "," + str(posy - 10)
            SendMessage(requestmovemessage)
            print(requestmovemessage)

        if keyboard.is_pressed('e'): # fire
            requestmovemessage = "fire:"
            SendMessage(requestmovemessage)
            print(requestmovemessage)

        if keyboard.is_pressed('x'): # bullet tornade (hopefully)
            for i in range(500):
                requestMessage = "facedirection:" + directions[i%8]
                SendMessage(requestMessage)
                print(requestmovemessage)
                requestMessage = "fire:"
                SendMessage(requestMessage)
                print(requestmovemessage)


main()    