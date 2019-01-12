import random
from colored import fore, back, style

from monster import Monster
import room_list

class Room:
    def __init__(self, location, data = None, monsterData = None):
        self.seen = False
        self.known = False
        self.hasContents = False
        self.monster = None
        self.trap = None
        self.stairs = ""
        if data:
            for k in data:
                setattr(self, k, data[k])
            if monsterData:
                self.monster = Monster(monsterData["level"], monsterData)
            else:
                self.monster = None
        else:
            self.generateName()
            self.hasContents = self.known

    def generateContents(self, dungeonLevel, floor = -1):
        if not self.hasContents:
            self.hasContents = True
            self.known = True
            if floor > -1: # boss monster
                self.monster = Monster(dungeonLevel - 1, { "floor": floor, "id": -1 })
            else:
                self.monster = Monster(dungeonLevel - 1)

    def generateName(self):
        descriptors = []
        descriptorKeys = random.sample(room_list.descriptor_types, random.randint(1, 2))

        for key in room_list.descriptor_types:
            if key in descriptorKeys:
                descriptors.append(random.choice(room_list.descriptors[key]))

        self.name = f"{fore.CYAN}A {' '.join(descriptors)} room"

    def printStats(self, exits):
        print(self.name + style.RESET)
        doors = []
        stairs = ""
        for exitDir, exitObj in exits:
            if exitObj.isValid():
                if exitDir == "n":
                    doors.append("North")
                if exitDir == "s":
                    doors.append("South")
                if exitDir == "e":
                    doors.append("East")
                if exitDir == "w":
                    doors.append("West")
                if exitDir == "up":
                    stairs = "There are stairs here going up."
                if exitDir == "down":
                    stairs = "There are stairs here going down."
        if len(doors) == 1:
            print(f"There is an exit to the {doors[0]}.")
        else:
            sliceObj = slice(len(doors) - 1)
            print(f"There are exits to the {', '.join(doors[sliceObj])} and {doors[len(doors) - 1]}.")
        if stairs:
            print(stairs)

    def getMapIcon(self):
        out = " "
        if self.monster and self.seen:
            out = f"{back.RED}{fore.WHITE}{self.monster.name[0]}{style.RESET}"
        return out

    def removeMonster(self):
        self.monster = None

    def printMap(self, isCurrentRoom, stairs = ""):
        out = ""
        wallColor = fore.WHITE
        if not self.known:
            wallColor = fore.BLACK
        elif stairs:
            wallColor = fore.RED if stairs == "down" else fore.GREEN
        if not self.seen:
            out += f"{style.DIM}"
        out += f"{wallColor}[{fore.WHITE}"
        out += "*" if isCurrentRoom else self.getMapIcon()
        out += f"{wallColor}]{fore.WHITE}{style.RESET}"
        return out