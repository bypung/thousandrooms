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

    def getMapIcon(self, monsterList):
        out = " "
        if self.monster and self.monster.known:
            monsterList.append(self.monster)
            out = f"{back.DARK_RED_1}{fore.ORANGE_3}{len(monsterList)}{style.RESET}"
        return out

    def removeMonster(self):
        self.monster = None

    def printMap(self, isCurrentRoom, monsterList, stairs = ""):
        out = ""
        wallColor = fore.WHITE
        if not self.known:
            wallColor = fore.BLACK
        elif stairs:
            wallColor = fore.RED if stairs == "down" else fore.GREEN
        if not self.seen:
            wallColor = f"{style.DIM}{wallColor}"
        out += f"{wallColor}[{style.RESET}"
        out += f"{back.NAVY_BLUE}{style.BOLD}*{style.RESET}" if isCurrentRoom else self.getMapIcon(monsterList)
        out += f"{wallColor}]{style.RESET}"
        return out