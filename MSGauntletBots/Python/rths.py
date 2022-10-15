# boilerplate
import socket
import time

import keyboard

msgFromClient = "requestjoin:rths"
name = "rths"

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
        update_map(map, msgFromServer)

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

# bmaa*

# initialise values
expansions = 8
vision = 5
moves = 8
push = False
flow = True

time = 0

if "playerupdate" in msgFromServer:
    pos = msgFromServer.split(":")[1]
    posSplit = pos.split(",")
    curr_node = [posSplit[0],posSplit[1]]

def controller():
    search_phase()
    if next_node:
        # move to next node
        requestmovemessage = "moveto: " + next_node[0] + "," + next_node[1]
    time += 1

def search_phase():
    if not next_node or time >= limit:
        search()
        if len(open_list) > 0:
            n = open_list[0]
            f = g + h
            update_heuristic_values(closed, f)
            limit = time + moves

def update_heuristic_values(closed, f):
    for n in closed:
        h = f - g

def search():
    P = []
    exp = 0
    closed = []
    open = [curr_node]
    map[curr_node[0],curr_node[1]] = 0

    while len(open_list) > 0:
        if open_list[0] == goal_node and exp >= expansions:
            #calculate P
            break
        n = open_list.pop(0)
        closed_list.append(n)

main()