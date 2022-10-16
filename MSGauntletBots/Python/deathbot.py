from crapbot import *
import socket
import time
import random
import numpy as np

# integrate Dave's path planning algo 
# run it on deathBot and check if we are detecting enemy direction and blasting them correctly 
 
msgFromClient       = "requestjoin:mydisplayname"
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

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def SendMessage(requestmovemessage):
    bytesToSend = str.encode(requestmovemessage)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def getPlayerCoords():
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    if "playerupdate" in msgFromServer:
        pos = msgFromServer.split(":")[1]
        posSplit = pos.split(",")
        posx = float(posSplit[0])
        posy = float(posSplit[1])
        posx = round(posx/8)
        posy = round(posy/8)
        print(f"My location has been retrieved at {(posx,posy)}")
        return int(posx),int(posy)

def enemyDirection(posx,posy):
    # character_class,name,posX,posY
    # detect enemy and take in enemy coords
    # work out which direction from me is the enemy at
        # playerPosX-enemyPosX, repeat for Y
        # if x+,y- or x+,y+ or x,y+, etccccc

    if "nearbyplayer" in msgFromServer: 
        pos = msgFromServer.split(":")[1]
        posSplit = pos.split(",")
        enemyx = float(posSplit[1])
        enemyy = float(posSplit[2])
        enemyx = int(round(enemyx/8))
        enemyy = int(round(enemyy/8))
    
    differencex = posx-enemyx 
    differencey = posy-enemyy

    if differencex==0 and (differencey/8)>0: #x,y+
        direction = "n"
    
    elif differencex==0 and (differencey/8)<0: #x,y-
        direction = "s"
    
    elif (differencex/8)>0 and differencey==0: #x+,y
        direction = "e"

    elif (differencex/8)<0 and differencey==0: #x-,y
        direction = "w"

    elif (differencex/8)>0 and (differencey/8)>0: #x+,y+
        direction = "ne"

    elif (differencex/8)>0 and (differencey/8)<0: #x+,y-
        direction = "se"

    elif (differencex/8)<0 and (differencey/8)<0: #x-,y-
        direction = "sw"
    
    elif (differencex/8)<0 and (differencey/8)>0: #x-,y+
        direction = "nw"

    print(f"The enemy is at my {direction}....")

    return direction


# turn that direction and start blasting 
def blastEnemy(direction):
    requestfacedirmessage = "facedirection:" + direction
    SendMessage(requestfacedirmessage)
    print(requestfacedirmessage)
    print(f"Facing {direction} and getting ready to blast...")

    requestblastmessage = "fire:"
    SendMessage(requestblastmessage)
    print(f"Firing at enemy at {direction} once!")

    requestblastmessage = "fire:"
    SendMessage(requestblastmessage)
    print(f"Firing at enemy at {direction} once more!")


floorsx = []
floorsy = []
wallsx = []
wallsy = []
grid = np.zeros((100,100))

while True:
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    #print(msgFromServer)
    if "playerjoined" in msgFromServer:
        bot_class = msgFromServer.split(":")[1].split(",")[0]
    
    if "nearbyfloors" in msgFromServer:
        floors = msgFromServer.split(":")[1]
        floors = list(map(int, floors.split(',')[:-1]))
        floorsx = (np.array(floors[::2])/8).astype(int)
        floorsy = (np.array(floors[1::2])/8).astype(int)
        for i in range(len(floorsx)):
            grid[floorsx[i], floorsy[i]] = 2
        findDoor(min(floorsx), max(floorsy))

    if "nearbywalls" in msgFromServer:
        walls = msgFromServer.split(":")[1]
        walls = list(map(int, walls.split(',')[:-1]))
        wallsx = np.array(walls[::2])//8
        wallsy = np.array(walls[1::2])//8
        for i in range(len(wallsx)):
            if grid[wallsx[i], wallsy[i]] <1:
                grid[int(wallsx[i]), int(wallsy[i])] = 1
    
    if "nearbyitem" in msgFromServer:
        item = isItem(msgFromServer)
        if(item):
            start = getCoords()
            path = astar(grid, start, item)
            print(path)
            if(path):
                print("found path to treasure")
                follow_path(path[::-1])

    elif(len(floorsx)!=0):
        randind = random.randrange(0,len(floorsx)-1)
        end = (floorsx[randind], floorsy[randind])
        start = getCoords()
        path = astar(grid, start, end)
        if(path):
            follow_path(path[::-1])
    
    posx,posy = getPlayerCoords()
    direction = enemyDirection(posx,posy)
    blastEnemy(direction)