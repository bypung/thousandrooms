import random

from colored import fore, back, style

from .monster import Monster
from .room_list import RoomList

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
        descriptorKeys = random.sample(RoomList.descriptor_types, random.randint(1, 2))

        for key in RoomList.descriptor_types:
            if key in descriptorKeys:
                descriptors.append(random.choice(RoomList.descriptors[key]))

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

    def printWall(self, side, stairs):
        if self.known:
            if stairs == "up":
                glyph = '<' if side == "left" else '>'
            elif stairs == "down":
                glyph = '{' if side == "left" else '}'
            else:
                glyph = '[' if side == "left" else ']'
        else:
            glyph = ' '
        
        wallColor = style.RESET
        wallStyle = ""
        if stairs:
            wallColor = fore.RED if stairs == "down" else fore.GREEN
            wallStyle = style.BOLD
        if not self.seen:
            wallStyle = style.DIM

        return f"{wallColor}{wallStyle}{glyph}{style.RESET}"

    def printMap(self, isCurrentRoom, monsterList, stairs = ""):
        out = ""
        out += self.printWall("left", stairs)
        out += f"{fore.WHITE}{back.BLUE}{style.BOLD}*{style.RESET}" if isCurrentRoom else self.getMapIcon(monsterList)
        out += self.printWall("right", stairs)
        return out