import numpy as np
import heapq
import matplotlib.pyplot as plt
import socket
import random
import time

msgFromClient       = "requestjoin:mydisplayname"
name = "mydisplayname"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

floorsx = []
floorsy = []
wallsx = []
wallsy = []
grid = np.zeros((100,100))
visited = []
exit = False
hasKey = False
key = False
lastLocation = [0,0]
isStuck =0
posx = 0
posy = 0
msgFromServer = ":"

pickups = {
    "treasure":[],
    "ammo":[],
    "food":[]
}
class_keys = {
    "warrior": "red",
    "elf": "green",
    "wizard": "yellow",
    "valkyrie": "blue"
}

bot_class = False

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def distanceFromLast(x,y):
    global lastLocation
    global isStuck
    if abs(x-lastLocation[0])>1 and abs(y-lastLocation[1])>1:
        lastLocation = [x, y]
        isStuck = 0
    else:
        isStuck +=1

def getCoords():
    global hasKey
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
        if "playerupdate" in msgFromServer:
            pos = msgFromServer.split(":")[1]
            posSplit = pos.split(",")
            hasKey = posSplit[4]
            posx = float(posSplit[0])
            posy = float(posSplit[1])
            posx = round(posx/8)
            posy = round(posy/8)
            distanceFromLast(posx, posy)
            return (int(posx), int(posy))


def heuristic(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(array, start, goal):
    neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
 
    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)

        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:   
                    if array[neighbor[0],neighbor[1]] < 2:
                        continue

                else:
                    # array bound y walls
                    continue

            else:
                # array bound x walls
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

def SendMessage(requestmovemessage):
    bytesToSend = str.encode(requestmovemessage)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def follow_path(coords):
    print("following coords", coords)
    i=0
    while i < len(coords):
        requestmovemessage = "moveto:" + str(coords[i][0]*8) + "," + str(coords[i][1]*8)
        SendMessage(requestmovemessage)
        getCoords()
        if isStuck:
            break
        dx = abs(posx - coords[i][0])
        dy = abs(posy - coords[i][1])
        if (0<=dx <1 and 0<=dy<1):
            i+=1
    SendMessage("stop:")
    updateFloors()

def isDoor(x,y):
    if (grid[x-1, y]==1 and grid[x, y]==2 and grid[x+1, y]==1):
        return True
    elif(grid[x, y-1]==1 and grid[x, y]==2 and grid[x, y+1]==1):
        return True
    else:
        return False

def findDoor(min, max):
    for x in range(min,max):
        for y in range(min,max):
            if grid[x,y]!=1:
                if isDoor(x,y):
                    if grid[x,y] <3:
                        grid[x,y] = 3

def isItem(msgFromServer):
    global key
    item = msgFromServer.split(":")[1].split(",")
    print(item)
    for i in range(0, len(item)-1, 3):
        if(class_keys[bot_class] in item):
            key = [int(item[1+i])//8, int(item[2+i])//8]
        elif "key" not in item[0+i]:
            pickups[item[0+i]].append(( int(item[1+i])//8, int(item[2+i])//8))

def updateFloors():
    while True:
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
        if "nearbyitem" in msgFromServer:
            isItem(msgFromServer)

        if "nearbyfloors" in msgFromServer:
            print("updating floors")
            floors = msgFromServer.split(":")[1]
            floors = list(map(int, floors.split(',')[:-1]))
            floorsx = (np.array(floors[::2])/8).astype(int)
            floorsy = (np.array(floors[1::2])/8).astype(int)
            for i in range(len(floorsx)):
                grid[floorsx[i], floorsy[i]] = 2
            return True

def go_to_position(target_pos_x, target_pos_y):
    requestmovemessage = "moveto:" + str(target_pos_x*8) + "," + str(target_pos_y*8)
    SendMessage(requestmovemessage)
    time.sleep(1)
    getCoords()
    if(abs(posx== target_pos_x)<1 and abs(posy-target_pos_y)<1):
        return False
    else:
        return True

def updatePosition(msgFromServer):
    global posx, posy, hasKey
    pos = msgFromServer.split(":")[1]
    posSplit = pos.split(",")
    hasKey = posSplit[4]
    posx = float(posSplit[0])
    posy = float(posSplit[1])
    posx = round(posx/8)
    posy = round(posy/8)
    distanceFromLast(posx, posy)

def updateExit(msgFromServer):
    exit = msgFromServer.split(":")[1].split(",")
    exit = [int(exit[0])//8, int(exit[1])//8]
    if hasKey:
        start = getCoords()
        path = astar(grid, start, exit)
        if(path):
            print("found path to exit")
            follow_path(path[::-1])

serverMessage = {
    "playerjoined": print,
    "playerupdate": updatePosition,
    "nearbywalls": False,
    "nearbyfloors": updateFloors,
    "nearbyitem": isItem,
    "nearbyplayer": False,
    "exit": updateExit
}

for p in range (100):
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
    print("start of loop", hasKey, key, isStuck, exit)
    #print(msgFromServer)
    if exit:
        start = getCoords()
        path = astar(grid, start, exit)
        if(path):
            print("found path to exit")
            follow_path(path[::-1])

    if "playerjoined" in msgFromServer:
        bot_class = msgFromServer.split(":")[1].split(",")[0]

    if "nearbyitem" in msgFromServer:
        item = isItem(msgFromServer)

    if "nearbyfloors" in msgFromServer:
        print("updating floors")
        floors = msgFromServer.split(":")[1]
        floors = list(map(int, floors.split(',')[:-1]))
        floorsx = (np.array(floors[::2])/8).astype(int)
        floorsy = (np.array(floors[1::2])/8).astype(int)
        for i in range(len(floorsx)):
            grid[floorsx[i], floorsy[i]] = 2
        #findDoor(min(floorsx), max(floorsy))

    if "nearbywalls" in msgFromServer:
        walls = msgFromServer.split(":")[1]
        walls = list(map(int, walls.split(',')[:-1]))
        wallsx = np.array(walls[::2])//8
        wallsy = np.array(walls[1::2])//8
        for i in range(len(wallsx)):
            if grid[wallsx[i], wallsy[i]] <1:
                grid[int(wallsx[i]), int(wallsy[i])] = 1
    
    if "nearbyitem" in msgFromServer:
        isItem(msgFromServer)
    
    if key:
        print(key)
        if not go_to_position(key[0], key[1]):
            start = (posx, posy)
            path = astar(grid, start, key)
            if(path):
                follow_path(path[::-1])
                key = False

    if(len(floorsx)!=0):
        randx = random.randrange(0,100, 2)
        randy = random.randrange(0,100, 2)
        end = (randx, randy)
        while(end in visited or (grid[randx, randy]<2)):
            randx = random.randrange(0,100)
            randy = random.randrange(0,100)
            end = (randx, randy)
        visited.append(end)
        if not go_to_position(randx, randy):
            start = (posx, posy)
            path = astar(grid, start, end)
            if(path):
                follow_path(path[::-1])

    # for pickup in pickups:
    #     if len(pickups[pickup])>0:
    #         for i in range(len(pickups[pickup])):
    #             if not go_to_position(pickups[pickup][i][0], pickups[pickup][i][1]):
    #                 start = getCoords()
    #                 path = astar(grid, start, pickups[pickup][i])
    #                 if(path):
    #                     follow_path(path[::-1])
        
plt.imshow(grid, cmap=plt.cm.Dark2)
plt.show()