import random
import copy
import sys
from colorama import Fore, Back, Style

from room import Room
from door import Door

class Map:
    def __init__(self, numFloors = 10, width = 10, data = None):
        self.floors = []
        self.width = width
        self.numFloors = numFloors
        self.dungeonLevel = 1 if not data else data["dungeonLevel"]

        for f in range(numFloors):
            floor = {
                "rooms": {},
                "doors": {
                    "ew": {},
                    "ns": {}
                },
                "stairs": {}
            }

            if data:
                for r in range(width):
                    for c in range(width):
                        # generate rooms
                        floor["rooms"][(r,c)] = Room((f, r, c), data["rooms"][f"{f}-{r}-{c}"], data["monsters"][f"{f}-{r}-{c}"])
                        # load east-west doors
                        if c < width - 1:
                            floor["doors"]["ew"][(r,c)] = Door("ew", data["doors"]["ew"][f"{f}-{r}-{c}"])
                        # load north-south doors
                        if r < width - 1:
                            floor["doors"]["ns"][(r,c)] = Door("ns", data["doors"]["ns"][f"{f}-{r}-{c}"])
                        # load stairs
                        try: 
                            floor["stairs"][(r,c)] = Door("stairs", data["stairs"][f"{f}-{r}-{c}"])
                        except KeyError:
                            pass
            else:
                for r in range(width):
                    for c in range(width):
                        # generate rooms
                        floor["rooms"][(r,c)] = Room((f, r, c))
                        # generate east-west doors
                        if c < width - 1:
                            floor["doors"]["ew"][(r,c)] = Door("ew")
                        # generate north-south doors
                        if r < width - 1:
                            floor["doors"]["ns"][(r,c)] = Door("ns")

                # connect rooms and doors
                for r in range(width):
                    for c in range(width):
                        doorList = []
                        if r > 0:
                            doorList.append(floor["doors"]["ns"][(r-1,c)])
                        if r < self.width - 1:
                            doorList.append(floor["doors"]["ns"][(r,c)])
                        if c > 0:
                            doorList.append(floor["doors"]["ew"][(r,c-1)])
                        if c < self.width - 1:
                            doorList.append(floor["doors"]["ew"][(r,c)])

                        # check for disconnected room and fix it
                        connected = False
                        for d in doorList:
                            if d.exists:
                                connected = True
                        if not connected:
                            random.choice(doorList).exists = True
            
                # generate stairs
                up = (-1, -1)
                if f > 0:
                    for i, (key, stair) in enumerate(self.floors[f - 1]["stairs"].items()):
                        if stair.stairDir == "down":
                            up = key
                            upStairs = copy.deepcopy(stair)
                            upStairs.stairDir = "up"
                            floor["stairs"][key] = upStairs
                if f < numFloors:
                    down = (random.randint(0,self.width - 1), random.randint(0,self.width - 1))
                    while down == up:
                        down = (random.randint(0,self.width - 1), random.randint(0,self.width - 1))
                    downStairs = Door("stairs")
                    downStairs.stairDir = "down"
                    floor["stairs"][down] = downStairs

            self.floors.append(floor)

        if data:
            self.playerPosition = data["playerPosition"]
        else:
            self.setPlayerPosition(0, -1, -1)
            escapeStairs = Door("stairs")
            escapeStairs.stairDir = "up"
            self.floors[0]["stairs"][(self.playerPosition[1], self.playerPosition[2])] = escapeStairs

    def getCurrentRoom(self):
        pp = self.playerPosition
        return self.floors[pp[0]]["rooms"][(pp[1],pp[2])]

    def getRoom(self, floor, row, col):
        return self.floors[floor]["rooms"][(row, col)]

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
        
        for key, door in self.getCurrentDoors():
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

    def printFloor(self, turn):
        floor = self.playerPosition[0]
        mapBuffer = []
        legendBuffer = [
            f"{Fore.CYAN}{Style.BRIGHT}Legend:", 
            f"{Fore.GREEN}[ ]{Fore.WHITE} / {Fore.RED}[ ]{Fore.WHITE} : Stairs Up/Down"
        ]

        ppSlug = f"[{self.playerPosition[1]},{self.playerPosition[2]}]"
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Dungeon Level {floor + 1} - Turn {turn}")

        # print top map header
        header = f"{Style.DIM}  "
        for c in range(self.width):
            header +=(f" {c} ")
            if (c < self.width - 1):
                header += "  "
        mapBuffer.append(header)

        # print map rows
        for r in range(self.width):
            roomRow = ""
            roomRow += f"{Style.DIM}{r} {Style.NORMAL}"
            for c in range(self.width):
                room = self.floors[floor]["rooms"][(r,c)]
                isCurrentRoom = self.playerPosition[1] == r and self.playerPosition[2] == c
                stairType = ""
                try:
                    stairs = self.floors[floor]["stairs"][(r,c)]
                    stairType = stairs.stairDir
                except KeyError:
                    pass
                roomRow += room.printMap(isCurrentRoom, stairType)
                if c < self.width - 1:
                    door = self.floors[floor]["doors"]["ew"][(r,c)]
                    roomRow += door.printMap()
            mapBuffer.append(roomRow)

            if r < self.width - 1:
                doorRow = "  "
                for c in range(self.width):
                    door = self.floors[floor]["doors"]["ns"][(r,c)]
                    doorRow += door.printMap()
                    if c < self.width - 1:
                        doorRow += "  "
                mapBuffer.append(doorRow)
        
        mapLineWidth = len(mapBuffer[0])
        for b in range(max(len(mapBuffer), len(legendBuffer))):
            mapLine = " " * mapLineWidth
            legendLine = ""
            try:
                mapLine = mapBuffer[b]
            except IndexError:
                pass
            try:
                legendLine = legendBuffer[b]
            except IndexError:
                pass
            print(f"{mapLine} {Style.DIM}| {Style.NORMAL}{legendLine}")

    def getCurrentDoors(self):
        floor = self.floors[self.playerPosition[0]]
        r = self.playerPosition[1]
        c = self.playerPosition[2]
        return self.getRoomDoors(floor, r, c)

    def getRoomDoors(self, floor, r, c):
        out = []
        if r > 0:
            out.append(("n", floor["doors"]["ns"][(r-1,c)]))
        if r < self.width - 1:
            out.append(("s", floor["doors"]["ns"][(r,c)]))
        if c > 0:
            out.append(("w", floor["doors"]["ew"][(r,c-1)]))
        if c < self.width - 1:
            out.append(("e", floor["doors"]["ew"][(r,c)]))
        for key, stair in floor["stairs"].items():
            if key == (r, c):
                out.append((stair.stairDir, stair))  
        return out

    def getOptions(self):
        out = f"{Style.BRIGHT}"
        options = []
        doors = []
        stairs = []
        for direction, door in self.getCurrentDoors():
            if (door.exists):
                if direction == "n":
                    doors += ["<N>orth"]
                if direction == "s":
                    doors += ["<S>outh"]
                if direction == "e":
                    doors += ["<E>ast"]
                if direction == "w":
                    doors += ["<W>est"]
                if direction == "up":
                    stairs += ["<U>p"]
                if direction == "down":
                    stairs += ["<D>own"]
        options += doors + stairs + ["<L>isten", "<S>earch", "<B>ack"]
        out += ", ".join(options)
        return out

