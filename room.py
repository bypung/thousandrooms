import random
from colorama import Fore, Back, Style

from monster import Monster
import room_list

class Room:
    def __init__(self, location, data = None, monsterData = None):
        if data:
            for k in data:
                setattr(self, k, data[k])
            if monsterData:
                self.monster = Monster(monsterData["level"], monsterData)
            else:
                self.monster = None
        else:
            self.generateName()
            self.seen = False
            self.known = False
            self.monster = None
            self.trap = None

    def generateContents(self, level):
        if not self.known:
            self.known = True
            self.monster = Monster(level)

    def generateName(self):
        descriptors = []
        descriptorKeys = random.sample(room_list.descriptor_types, random.randint(1, 2))

        for key in room_list.descriptor_types:
            if key in descriptorKeys:
                descriptors.append(random.choice(room_list.descriptors[key]))

        self.name = f"{Fore.CYAN}A {' '.join(descriptors)} room"

    def printStats(self, exits):
        print(self.name)
        doors = []
        stairs = ""
        for exitDir, exitObj in exits:
            if exitObj.exists:
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
            out = f"{Back.RED}{Fore.WHITE}{self.monster.name[0]}{Style.RESET_ALL}"
        return out

    def removeMonster(self):
        self.monster = None

    def printMap(self, isCurrentRoom, stairs = ""):
        out = ""
        wallColor = Fore.WHITE
        if not self.known:
            wallColor = Fore.BLACK
        elif stairs:
            wallColor = Fore.RED if stairs == "down" else Fore.GREEN
        if not self.seen:
            out += f"{Style.DIM}"
        out += f"{wallColor}[{Fore.WHITE}"
        out += "*" if isCurrentRoom else self.getMapIcon()
        out += f"{wallColor}]{Fore.WHITE}{Style.NORMAL}"
        return out