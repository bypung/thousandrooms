from colorama import Fore, Back, Style

from creature import Creature
from item import Item
from utils import Utils

class Player(Creature):
    def __init__(self, name, saveInfo = None):
        info = saveInfo if saveInfo else {
            "name": name,
            "level": 1,
            "nextLevel": 1000,
            "atk": 1,
            "ac": 10,
            "hp": 10,
            "maxHp": 10,
            "xp": 0,
            "gp": 0,
            "items": [],
            "history": {
                "rest": 0,
                "risky_win": 0,
                "run_away": 0,
                "kills": 0,
                "sold_item": 0,
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

    def addItem(self, item):
        # auto-equip item if no item of this type is equipped
        itemType = item.type
        found = False
        for invItem in self.items:
            if invItem.type == itemType:
                found = True
        if not found:
            item.equipped = True

        self.items.append(item)
        self.applyItems()
        
    def equipItem(self, newItemIndex):
        oldItemIndex = -1

        newItem = self.items[newItemIndex]

        for i, invItem in enumerate(self.items):
            if invItem.type == newItem.type and invItem.equipped:
                oldItemIndex = i
        self.items[oldItemIndex].equipped = False
        newItem.equipped = True

        self.applyItems()
        
    def applyItems(self):
        self.atk = 1
        self.ac = 10

        for item in self.items:
            if item.equipped:
                self.atk += item.atk
                self.ac += item.ac

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

    def incrementHistory(self, field, value = 1):
        self.history[field] += value

    def setEpitaph(self, monster, level):
        self.history["epitaph"] = f"Killed by a {monster.name} on level {level}."

    def printStats(self):
        print(f"{Fore.BLUE}{Style.BRIGHT}{self.name}")

        hpColor = Fore.WHITE
        if self.hp / self.maxHp <= .6:
            hpColor = Fore.YELLOW
        elif self.hp / self.maxHp <= .25:
            hpColor = Fore.RED

        stats = [
            {
                "Level": f"{self.level}",
                "XP": f"{self.xp} / {self.nextLevel}",
                "GP": f"{self.gp}"
            },
            {
                "HP": f"{hpColor}{self.hp}{Fore.WHITE} / {self.maxHp}    ",
                "ATK": f"{self.atk} ({self.dam})",
                "AC": f"{self.ac}",
            }
        ]
        Utils.printStats(stats)
        
        itemNames = []
        if len(self.items) == 0:
            itemNames = ["None"]
        for item in self.items:
            if item.equipped:
                itemNames.append(item.name)
        print("Equipped: " + ", ".join(itemNames))

    def printInventory(self):
        print(f"{Fore.BLUE}{Style.BRIGHT}Inventory")

        items = []
        
        for i, item in enumerate(self.items, 1):
            items.append({
                "_color": Fore.GREEN if item.equipped else Fore.WHITE,
                "Name": f"{i}) {item.name}",
                "ATK": f"{item.atk if item.atk > 0 else '--'}",
                "AC": f"{item.ac if item.ac > 0 else '--'}",
                "Value": f"{item.level * 10}"
            })

        Utils.printTable(["   Name", "ATK", "AC", "Value"], items)

    def printHistory(self):
        print(f"{Fore.BLUE}{Style.BRIGHT}History")
        print(f"{Fore.RED}{self.history['epitaph']}")

        stats = [
            { 
                "Times Rested": f"{self.history['rest']}",
                "Battles Fled": f"{self.history['run_away']}"
            },
            {
                "Kills": f"{self.history['kills']}",
                "Risky Wins": f"{self.history['risky_win']}" 
            },
            { 
                "Items Sold": f"{self.history['sold_item']}" 
            },
            { 
                "Damage Done": f"{self.history['dmg_done']}",
                "Damage Taken": f"{self.history['dmg_taken']}" 
            },
        ]
        Utils.printStats(stats)
