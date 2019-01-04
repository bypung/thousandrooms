import random
from colorama import Fore, Back, Style

from monster import Monster

class Room:
    def __init__(self, data = None, monsterData = None):
        if data:
            for k in data:
                setattr(self, k, data[k])
            if monsterData:
                self.monster = Monster(monsterData["level"], monsterData)
            else:
                self.monster = None
        else:
            self.type = random.choice(["A", "B", "C", "D"])
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
        print("An empty room.")

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