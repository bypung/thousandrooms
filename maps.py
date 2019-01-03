import random
import sys
from colorama import Fore, Back, Style

from room import Room
from door import Door

class Map:
    def __init__(self, numFloors = 10, width = 10):
        self.floors = []
        self.width = width
        self.numFloors = numFloors
        self.dungeonLevel = 1

        for f in range(numFloors):
            floor = {
                "rooms": [],
                "doors": {
                    "ew": [],
                    "ns": []
                }
            }

            # generate rooms
            for r in range(width):
                row = []
                for c in range(width):
                    row.append(Room(f + 1))
                floor["rooms"].append(row)
            self.floors.append(floor)

            # generate east-west doors
            for r in range(width):
                row = []
                for c in range(width - 1):
                    row.append(Door(f + 1, "ew"))
                floor["doors"]["ew"].append(row)
            self.floors.append(floor)

            # generate north-south doors
            for r in range(width - 1):
                row = []
                for c in range(width):
                    row.append(Door(f + 1, "ns"))
                floor["doors"]["ns"].append(row)

            # connect rooms and doors
            for r in range(width):
                for c in range(width):
                    # add doors to room object
                    room = floor["rooms"][r][c]
                    if r > 0:
                        room.doors["n"] = floor["doors"]["ns"][r-1][c]
                    if r < self.width - 1:
                        room.doors["s"] = floor["doors"]["ns"][r][c]
                    if c > 0:
                        room.doors["w"] = floor["doors"]["ew"][r][c-1]
                    if c < self.width - 1:
                        room.doors["e"] = floor["doors"]["ew"][r][c]

                    # check for disconnected room and fix it
                    connected = False
                    for d in room.doors:
                        if room.doors[d].exists:
                            connected = True
                    if not connected:
                        room.doors[random.choice(list(room.doors))].exists = True
            
            self.floors.append(floor)

        self.setPlayerPosition(0, -1, -1)

    def getCurrentRoom(self):
        pp = self.playerPosition
        return self.floors[pp[0]]["rooms"][pp[1]][pp[2]]

    def getRoom(self, floor, row, col):
        return self.floors[floor]["rooms"][row][col]

    def movePlayer(self, direction):
        newPos = list(self.playerPosition)
        if direction == "n":
            newPos[1] -= 1
        elif direction == "s":
            newPos[1] += 1
        elif direction == "e":
            newPos[2] += 1
        elif direction == "w":
            newPos[2] -= 1
        elif direction == "u":
            newPos[0] -= 1
        elif direction == "d":
            newPos[0] += 1
        
        self.setPlayerPosition(newPos[0], newPos[1], newPos[2])

    def setPlayerPosition(self, floor, row, col):
        startRoom = False
        if row == -1 or col == -1:
            startRoom = True
            row = random.randint(0, self.width -1)
            col = random.randint(0, self.width - 1)
        self.playerPosition = [floor, row, col]
        
        room = self.getRoom(floor, row, col)
        room.seen = True
        room.known = True

        if startRoom:
            room.monster = None
        
        for key in room.doors.keys():
            door = room.doors[key]
            door.seen = True
            if (door.exists):
                if key == "n":
                    self.getRoom(floor, row - 1, col).generateContents(self.dungeonLevel)
                if key == "s":
                    self.getRoom(floor, row + 1, col).generateContents(self.dungeonLevel)
                if key == "e":
                    self.getRoom(floor, row, col + 1).generateContents(self.dungeonLevel)
                if key == "w":
                    self.getRoom(floor, row, col - 1).generateContents(self.dungeonLevel)

    def printFloor(self):
        floor = self.playerPosition[0]
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Dungeon Level {floor + 1}")

        header = f"{Style.DIM}  "
        for c in range(self.width):
            header +=(f" {c} ")
            if (c < self.width - 1):
                header += "  "
        print(header)

        for r in range(self.width):
            sys.stdout.write(f"{Style.DIM}{r} {Style.NORMAL}")
            for c in range(self.width):
                room = self.floors[floor]["rooms"][r][c]
                isCurrentRoom = self.playerPosition[1] == r and self.playerPosition[2] == c
                sys.stdout.write(room.printMap(isCurrentRoom))
                if c < self.width - 1:
                    door = self.floors[floor]["doors"]["ew"][r][c]
                    sys.stdout.write(door.printMap())
            if r < self.width - 1:
                sys.stdout.write("\n  ")
                for c in range(self.width):
                    door = self.floors[floor]["doors"]["ns"][r][c]
                    sys.stdout.write(door.printMap())
                    if c < self.width - 1:
                        sys.stdout.write("  ")
            sys.stdout.write("\n")

    def getOptions(self):
        out = f"{Style.BRIGHT}"
        room = self.getCurrentRoom()
        for key in room.doors.keys():
            door = room.doors[key]
            if (door.exists):
                if key == "n":
                    out += "<N>orth, "
                if key == "s":
                    out += "<S>outh, "
                if key == "e":
                    out += "<E>ast, "
                if key == "w":
                    out += "<W>est, "
        out += "<L>isten, <S>earch, <B>ack"
        return out

