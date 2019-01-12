import random

from colored import fore, back, style

import monster_list
from creature import Creature
from utils import Utils

class Monster(Creature):
    def __init__(self, level, data = None):
        level = random.randint(max(1, level - 1), level + 1)
        self.charged = False
        if data:
            for k in data:
                setattr(self, k, data[k])
        else:
            info = self.getMonster(level)
            Creature.__init__(self, info)

            # improved monsters
            levelDiff = level - self.level
            if levelDiff > 0:
                descriptor = monster_list.descriptors[self.type][levelDiff - 1]
                try:
                    descriptor = monster_list.descriptors[self.subtype][levelDiff - 1]
                except KeyError:
                    pass
                self.name = f"{descriptor} {self.name}"
                self.level += levelDiff
                self.atk += levelDiff

            self.hp = 0
            for x in range(level):
                self.hp += random.randint(1, self.hd)
            
            self.ac += 10 + levelDiff
                    
    def printStats(self):
        print(f"{fore.RED}{style.BOLD}{self.name} ({str(self.level)}){style.RESET}")
        stats = [
            {
                "HP": f"{self.hp}",
                "ATK": f"{self.atk} {Creature.calculateDam(self)}",
                "AC": f"{self.ac}"
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

