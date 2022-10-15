import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import socket
import random
import time

msgFromClient = "requestjoin:bot"
name = "bot"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = ("127.0.0.1", 11000)

bufferSize          = 1024

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)

def SendMessage(requestmovemessage):
    bytesToSend = str.encode(requestmovemessage)
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

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
                    if array[neighbor[0],neighbor[1]] == 1:
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

def follow_path(coords, posx, posy):
    for i in range(len(coords)-1, 0, -1):
        if coords[i][0]*8 != posx and coords[i][1]*8 != posy:
            requestmovemessage = "moveto:" + str(coords[i][0]*8) + "," + str(coords[i][1]*8)
            SendMessage(requestmovemessage)

floorsx = []
floorsy = []
wallsx = []
wallsy = []
itemsx = []
itemsy = []

chosen_floor_indices = []
chosen_item_indices = []

wallmap = np.zeros((100,100))

grid = wallmap

a = 0
while True:
    while(len(wallsx) == 0 or len(floorsx) == 0):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
        if "nearbywalls" in msgFromServer:
                walls = msgFromServer.split(":")[1]
                walls = list(map(int, walls.split(',')[:-1]))
                wallsx = np.array(walls[::2])//8
                wallsy = np.array(walls[1::2])//8
                for i in range(len(wallsx)):
                    if wallmap[wallsx[i], wallsy[i]] < 1:
                        wallmap[int(wallsx[i]), int(wallsy[i])] = 1

        if "nearbyfloors" in msgFromServer:
            floors = msgFromServer.split(":")[1]
            floors = list(map(int, floors.split(',')[:-1]))
            floorsx = np.array(floors[::2])//8
            floorsy = np.array(floors[1::2])//8
            for i in range(len(floorsx)):
                if wallmap[floorsx[i], floorsy[i]] < 1:
                    wallmap[int(floorsx[i]), int(floorsy[i])] = 2

        if "nearbyitems" in msgFromServer:
            items = msgFromServer.split(":")[1]
            items = list(map(int, floors.split(',')[:-1]))
            itemsx = np.array(items[::2])//8
            itemsy = np.array(items[1::2])//8
            for i in range(len(itemsx)):
                if wallmap[itemsx[i], itemsy[i]] < 3:
                    wallmap[int(itemsx[i]), int(itemsy[i])] = 3

    start = (0,0)
    while start == (0,0):
        msgFromServer = UDPClientSocket.recvfrom(bufferSize)[0].decode('ascii')
        if "playerupdate" in msgFromServer:
            pos = msgFromServer.split(":")[1]
            print("position:", pos)
            posSplit = pos.split(",")
            posx = float(posSplit[0])
            posy = float(posSplit[1])
            posx = round(posx/8)
            posy = round(posy/8)
            start = (int(posx), int(posy))

    if len(itemsx) > 0:
        index = random.randint(0, len(items)-1)
        while index in chosen_item_indices:
            index = random.randint(0, len(items)-1)
        
        chosen_item_indices.append(index)
        goal = (itemsx[index],itemsy[index])

    else:
        index = random.randint(0, len(floorsx)-1)
        while index in chosen_floor_indices:
            index = random.randint(0, len(floorsx)-1)

        chosen_floor_indices.append(index)
        goal = (floorsx[index],floorsy[index])

    route = astar(grid, start, goal)

    route = route + [start]

    route = route[::-1]

    follow_path(route, posx, posy)

    print(route)

    a += 1
    print(a)

    if a > 50:
        time.sleep(1)
        a = 0