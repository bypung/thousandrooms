import random

from colored import fore, back, style

from .monster_list import MonsterList
from .creature import Creature
from .utils import Utils

class Monster(Creature):
    distribution = [0,0,0,0,0,0,0,1,1,1,1,1,2,2,2,1,3,3,3,4,4,5,5,6,6,7,7]

    def __init__(self, dungeonLevel, data = None):
        genlevel = random.randint(max(1, dungeonLevel - 1), dungeonLevel + 1)
        self.charges = 0
        self.chargeRate = 1
        self.isBoss = False
        self.quotes = None
        self.seen = False
        self.known = False
        isBoss = data and data["id"] < 0
        if data and not isBoss:
            for k in data:
                setattr(self, k, data[k])
            try:
                test = self.displayName
            except AttributeError:
                self.displayName = self.name
        else:
            monsterLevel = data["floor"] + 1 if isBoss else genlevel
            info = self.getMonster(monsterLevel)
            Creature.__init__(self, info)
            self.level = monsterLevel
            self.ac += 10
            self.displayName = self.name

            if isBoss:
                # generate boss monster
                self.isBoss = True

                descriptor = random.choice(MonsterList.bossDescriptors[self.type])
                try:
                    descriptor = random.choice(MonsterList.bossDescriptors[self.subtype])
                except KeyError:
                    pass
                if descriptor[0]:
                    self.displayName = f"{descriptor[0]} {self.displayName}"
                if descriptor[1]:
                    self.displayName += f" {descriptor[1]}"

                self.quotes = MonsterList.bossQuotes[self.type]
                try:
                    self.quotes = MonsterList.bossQuotes[self.subtype]
                except KeyError:
                    pass

                diffFactor = max(dungeonLevel, data["floor"]) + 2
                self.chargeRate = 2
                self.level += diffFactor
                self.atk += diffFactor
                self.ac += diffFactor
                self.maxHp = self.hd * self.level
                self.hp = self.hd * self.level
            else:
                # improved monsters
                levelDiff = dungeonLevel - self.level
                if levelDiff > 0:
                    descriptor = MonsterList.descriptors[self.type][levelDiff // 2]
                    try:
                        descriptor = MonsterList.descriptors[self.subtype][levelDiff // 2]
                    except KeyError:
                        pass
                    self.displayName = f"{descriptor} {self.displayName}"
                    self.level += levelDiff
                    self.atk += 2 * levelDiff
                    self.ac += 2 * levelDiff    
                    self.hd += levelDiff    

                self.maxHp = self.hd * self.level
                self.hp = 0
                for x in range(self.level):
                    self.hp += random.randint(self.hd // 2, self.hd)
                                    
    def printStats(self, playerLore):
        nameColor = fore.DARK_ORANGE_3B if self.isBoss else fore.RED
        print(f"{nameColor}{style.BOLD}{self.displayName} ({str(self.level)}){style.RESET}")
        try:
            lore = playerLore[str(self.id)]
        except KeyError:     
            lore = { "resist": False, "vulnerability": False, "special": False}

        unknown = f"{style.DIM}???{style.RESET}"
        resist = self.resist if self.resist else "---"
        vulnerability = self.vulnerability if self.vulnerability else "---"
        special = self.special if self.special else "extra attack"

        stats = [
            {
                "HP": f"{self.hp}",
                "ATK": f"{self.atk} {Creature.calculateDam(self)}",
                "AC": f"{self.ac}"
            },
            {
                "Resists": resist if lore["resist"] else unknown,
                "Vulnerability": vulnerability if lore["vulnerability"] else unknown,
                "Special Attack": special if lore["special"] else unknown
            }
        ]
        Utils.printStats(stats)

    def getAtkVerb(self):
        verbs = MonsterList.atkVerbs[self.atk_type]
        try:
            verbs = MonsterList.atkVerbs[self.type][self.atk_type]
        except KeyError:
            pass
        try:
            verbs = MonsterList.atkVerbs[self.subtype][self.atk_type]
        except KeyError:
            pass
        return random.choice(verbs)

    @staticmethod
    def getMonster(level):
        randomLevel = 0
        while randomLevel <= 0:
            randomLevel = level - random.choice(Monster.distribution)
        monsters = [monster for monster in MonsterList.monsters if monster["level"] == randomLevel] 
        info = random.choice(monsters)
        return info

