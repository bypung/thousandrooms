import random

from colorama import Fore, Back, Style

class Door:
    def __init__(self, doorType, data = None):
        if data:
            for k in data:
                setattr(self, k, data[k])
        else:
            self.type = doorType
            self.exists = random.choice([True, True, False])
            self.seen = False
            self.used = False

    def printStats(self):
        print("<< Door >>")

    def useDoor(self):
        self.used = True

    def isValid(self):
        return True if self.type == "stairs" else self.exists

    def printMap(self):
        out = Fore.WHITE if self.exists and self.seen else Fore.BLACK
        out += "==" if self.type == "ew" else " | "
        out += Fore.RESET
        return out