import random

from colorama import Fore, Back, Style

class Door:
    def __init__(self, level, doorType):
        self.level = level
        self.type = doorType
        self.exists = random.choice([True, True, False])
        self.seen = False

    def printStats(self):
        print("<< Door >>")
        print(f"Level: {self.level}")

    def printMap(self):
        out = Fore.WHITE if self.exists and self.seen else Fore.BLACK
        out += "==" if self.type == "ew" else " | "
        out += Fore.RESET
        return out