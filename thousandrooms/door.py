import random

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
        if self.exists and self.seen:
            return "==" if self.type == "ew" else " | "
        else:
            return "  " if self.type == "ew" else "   "
