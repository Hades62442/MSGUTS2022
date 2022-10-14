import socket
import time
import random

import keyboard  # using module keyboard

msgFromClient = "requestjoin:mydisplayname"
name = "mydisplayname"

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

        if keyboard.is_pressed('j'): # move left
            requestmovemessage = "moveto:" + str(posx - 10)  + "," + str(posy)
            SendMessage(requestmovemessage)

        if keyboard.is_pressed('k'): # move down
            requestmovemessage = "moveto:" + str(posx)  + "," + str(posy + 10)
            SendMessage(requestmovemessage)

        if keyboard.is_pressed('l'): # move right
            requestmovemessage = "moveto:" + str(posx + 10)  + "," + str(posy)
            SendMessage(requestmovemessage)

        if keyboard.is_pressed('i'): # move up
            requestmovemessage = "moveto:" + str(posx)  + "," + str(posy - 10)
            SendMessage(requestmovemessage)

        if keyboard.is_pressed('o'): # fire
            requestmovemessage = "fire:"
            SendMessage(requestmovemessage)

        if keyboard.is_pressed('p'): # bullet tornade (hopefully)
            for i in range(500):
                requestMessage = "facedirection:" + directions[i%8]
                SendMessage(requestMessage)
                requestMessage = "fire:"
                SendMessage(requestMessage)


main()    