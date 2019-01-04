import random

from colorama import Fore, Back, Style

import monster_list
from creature import Creature
from utils import Utils

class Monster(Creature):
    def __init__(self, level, data = None):
        if data:
            for k in data:
                setattr(self, k, data[k])
        else:
            info = self.getMonster(level)
            Creature.__init__(self, info)

            # improved monsters
            levelDiff = level - self.level
            if levelDiff > 0:
                self.name = f"{monster_list.descriptors[self.type][levelDiff]} {self.name}"
                self.level += levelDiff

            self.hp = 0
            for x in range(level):
                self.hp += random.randint(1, self.hd)
            
            self.ac += 10 + levelDiff
                    
    def printStats(self):
        print(f"{Fore.RED}{Style.BRIGHT}{self.name} ({str(self.level)})")
        stats = [
            {
                "HP": str(self.hp),
                "ATK": f"{str(self.atk)} ({str(self.dam)})",
                "AC": str(self.ac),
            }
        ]
        Utils.printStats(stats)

    def getAtkVerb(self):
        verbs = monster_list.atkVerbs[self.type][self.atk_type]
        return random.choice(verbs)

    @staticmethod
    def getMonster(level):
        monsters = [monster for monster in monster_list.monsters if monster["level"] <= level and monster["level"] > level - 5] 
        info = random.choice(monsters)
        return info

