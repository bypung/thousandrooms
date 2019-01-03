class Room:
    def __init__(self, player):
        self.level = player.level

    def printStats(self):
        print("<< Room >>")
        print("Level: " + str(self.level))