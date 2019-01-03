import random
from colorama import Fore, Back, Style

from monster import Monster

class Room:
    def __init__(self, level):
        self.level = level
        self.type = random.choice(["A", "B", "C", "D"])
        self.doors = {}
        self.seen = False
        self.known = False
        self.monster = None
        self.trap = None

    def generateContents(self, level):
        if not self.known:
            self.known = True
            self.monster = Monster(level)

    def printStats(self):
        print("<< Room >>")
        print("Level: " + str(self.level))

    def getMapIcon(self):
        return " "

    def removeMonster(self):
        self.monster = None

    def printMap(self, isCurrentRoom):
        out = ""
        if not self.known:
            out += f"{Fore.BLACK}"  
        if not self.seen:
            out += f"{Style.DIM}"
        out += "["
        out += "*" if isCurrentRoom else self.getMapIcon()
        out += f"]{Fore.WHITE}{Style.NORMAL}"
        return out