import random
import copy

from colored import fore, back, style

from .creature import Creature
from .item import Item
from .utils import Utils
from .item_list import ItemList

class Player(Creature):
    def __init__(self, name, saveInfo = None):
        self.level = 1
        self.xp = 0
        self.gp = 0
        self.hp = 0
        self.ac = 10
        self.maxHp = 0
        self.history = {}
        self.name = name
        self.nextLevel = 100
        self.items = []
        self.skills = []
        self.innateAbilities = {}
        self.abilities = {}
        self.conditions = {}
        self.resist = []
        self.monsterLore = {}
        self.hasIdol = False
        
        info = saveInfo if saveInfo else {
            "name": name,
            "level": 1,
            "nextLevel": 1000,
            "atk": 1,
            "hp": 10,
            "maxHp": 10,
            "atkType": 'blunt',
            "history": {
                "rest": 0,
                "risky_win": 0,
                "reckless": 0,
                "run_away": 0,
                "kills": 0,
                "buy_item": 0,
                "sell_item": 0,
                "dmg_done": 0,
                "dmg_taken": 0,
                "epitaph": "Still exploring..."
            }
        }
        Creature.__init__(self, info)

    def loadItems(self, itemData):
        self.items = []
        for data in itemData:
            self.items.append(Item(0, data))

    def addGold(self, value):
        self.gp += value
        
    def removeGold(self, value):
        self.gp -= value

    def addItem(self, item):
        # auto-equip item if no item of this type is equipped
        kind = item.kind
        if kind == "usable":
            found = False
            for invItem in self.items:
                if invItem.id == item.id:
                    found = True
                    invItem.stack += 1
            if not found:
                self.items.append(item)
        else:
            found = False
            for invItem in self.items:
                if invItem.kind == kind:
                    found = True
            if not found:
                item.equipped = True
            self.items.append(item)
            self.applyItems()
        
    def removeItem(self, item):
        if item.kind == "usable" and item.stack > 1:
            item.stack -= 1
        else:
            self.items.remove(item)
        self.applyItems()
        
    def equipItem(self, newItem):
        for invItem in self.items:
            if invItem.kind == newItem.kind and invItem.equipped:
                invItem.equipped = False
        newItem.equipped = True

        self.applyItems()
        
    def unequipItem(self, kind):
        for invItem in self.items:
            if invItem.kind == kind and invItem.equipped:
                invItem.equipped = False
        self.applyItems()
        
    def applyItems(self):
        self.atk = (self.level + 1) // 2
        self.ac = 10
        self.abilities = copy.copy(self.innateAbilities)
        self.resist = []
        self.atkType = "blunt"

        for item in self.items:
            if item.equipped:
                if item.atk:
                    self.atk += item.atk
                if item.ac:
                    self.ac += item.ac
                if item.kind == "weapon":
                    self.atkType = item.type
                if item.ability:
                    if "resist_" in item.ability:
                        self.resist.append(item.ability.replace("resist_", ""))
                    else:
                        try: 
                            self.abilities[item.ability] += item.getAbilityLevel()
                        except KeyError:
                            self.abilities[item.ability] = item.getAbilityLevel()

        super().calculateDam()

    def checkLevelUp(self):
        if self.xp >= self.nextLevel:
            self.level += 1
            self.hp += 10
            self.maxHp += 10
            self.nextLevel += 1000 * self.level
            self.applyItems()
            return True
        else:
            return False

    def getAbilityLevel(self, ability):
        level = 0
        try:
            level = self.abilities[ability]
        except KeyError:
            pass
        return level

    def getAtkVerb(self):
        verbs = ItemList.atkVerb[self.atkType]
        return random.choice(verbs)
        
    def incrementHistory(self, field, value = 1):

        self.history[field] += value

    def drain(self, value):
        self.xp -= value
        if self.xp < 0:
            self.xp = 0
            
    def killedBy(self, monster, level):
        self.setEpitaph(f"Killed by a {monster.name} on level {level}.")

    def setEpitaph(self, text):
        self.history["epitaph"] = text

    def printStats(self):
        print(f"{fore.MAGENTA}{style.BOLD}{self.name}{style.RESET}")

        hpColor = style.RESET
        if self.hp / self.maxHp <= .25:
            hpColor = fore.RED
        elif self.hp / self.maxHp <= .6:
            hpColor = fore.YELLOW

        stats = [
            {
                "Level": f"{self.level}",
                "XP": f"{self.xp} / {self.nextLevel}",
                "GP": f"{self.gp}"
            },
            {
                "HP": f"{hpColor}{self.hp}{style.RESET} / {self.maxHp}",
                "ATK": f"{self.atk} {Creature.calculateDam(self)}",
                "AC": f"{self.ac}",
            }
        ]
        Utils.printStats(stats)
        
        itemNames = []
        if len(self.items) == 0:
            itemNames = ["None"]
        for item in self.items:
            if item.equipped:
                itemNames.append(item.displayName)
        print("Equipped: " + ", ".join(itemNames))

    def getLoreRating(self, floor):
        maxLore = (floor + 1) * 12
        count = 0
        for key, m in self.monsterLore.items():
            if m["resist"]:
                count += 1
            if m["vulnerability"]:
                count += 1
            if m["special"]:
                count += 1
        return count / maxLore * 100

    def hasSeenMonster(self, monster):
        try:
            lore = self.monsterLore[monster.id]
            return True
        except KeyError:
            return False

    def printHistory(self, turns):
        print(f"{fore.MAGENTA}{style.BOLD}{self.name}{style.RESET}")
        print(f"{fore.RED}{self.history['epitaph']}{style.RESET}\n")

        stats = [
            { 
                "Total Turns": f"{turns}",
                "Times Rested": f"{self.history['rest']}",
                "Battles Fled": f"{self.history['run_away']}"
            },
            {
                "Kills": f"{self.history['kills']}",
                "Reckless Attacks": f"{self.history['reckless']}",
                "Risky Wins": f"{self.history['risky_win']}" 
            },
            { 
                "Items Bought": f"{self.history['buy_item']}",
                "Items Sold": f"{self.history['sell_item']}" 
            },
            { 
                "Damage Done": f"{self.history['dmg_done']}",
                "Damage Taken": f"{self.history['dmg_taken']}" 
            },
        ]
        Utils.printStats(stats)
