import random

from colored import fore, back, style

import item_list
from utils import Utils

class Item:
    def __init__(self, level, data = None):
        if level > 0:
            self.level = level
            self.equipped = False
            self.kind = ''
        
        if data:
            for i in data:
                setattr(self, i, data[i])
        else:
            info = self.getItem(level)
            if info != None:
                for i in info:
                    setattr(self, i, info[i])
                
                if self.ability:
                    self.displayName = f"{self.name} of {self.ability.title()}"
                elif self.effect:
                    self.displayName = f"{self.name} of {self.effect.title()}"
                else:
                    self.displayName = self.name

                # improved items
                if self.kind != "usable":
                    levelDiff = level - self.level
                    if levelDiff > 0:
                        try:
                            descriptor = item_list.descriptors[self.kind][levelDiff - 1]
                        except KeyError:
                            pass
                        try:
                            descriptor = item_list.descriptors[self.kind][self.type][levelDiff - 1]
                        except KeyError:
                            pass
                        except TypeError:
                            pass
                        self.displayName = f"{descriptor} {self.displayName}"
                        self.level += levelDiff
                        if self.atk:
                            self.atk += levelDiff
                        if self.ac:
                            self.ac += levelDiff

                if self.kind in ["weapon", "armor"]:
                    egoChance = random.randint(1,100)
                    if egoChance <= level:
                        self.generateEgo()

    def generateEgo(self):
        if self.kind == "weapon":
            ego = random.choice(item_list.weaponEgo)
            self.atk += ego["bonus"]
        else:
            ego = random.choice(item_list.armorEgo)
            self.ac += ego["bonus"]

        self.displayName += f" of {ego['name']}"
        for key in ego["attributes"]:
            setattr(self, key, ego["attributes"][key])

    @staticmethod
    def getItem(level):
        itemRoll = random.randint(level, 100)
        kind = "none"
        
        if itemRoll < 80:
            return None
        if itemRoll < 88:
            kind = "usable"
        elif itemRoll < 93:
            kind = "weapon"
        elif itemRoll < 98:
            kind = "armor"
        else:
            kind = "ring"
    
        if kind in ["usable", "ring"]:
            items = [item for item in item_list.items if item["kind"] == kind and item["level"] <= level] 
        else:
            items = [item for item in item_list.items if item["kind"] == kind and item["level"] <= level and item["level"] > level - 5] 
        info = random.choice(items)
        return info

    @staticmethod
    def getOptions(source, options):
        page = options["currPage"]
        pageSize = options["pageSize"]
        filterValue = options["filter"]
        mode = options["mode"]
        message = options["message"]
        if mode in ["buy", "sell"]:
            message = f"{fore.YELLOW}GP: {options['gp']}  {style.RESET}{message}"
        sourceType = type(source).__name__
        actions = []
        if sourceType == "Player":
            if mode == "combat":
                actions = ["<U>se"]  
            elif mode == "sell":
                actions = ["<B>uy", "<S>ell"]  
            else:
                actions = ["<E>quip", "<U>se"]
        elif sourceType == "Store":
            actions = ["<B>uy", "<S>ell"]
        
        filteredItems = source.items if filterValue == "all" else list(filter(lambda i: i.kind == filterValue, source.items))
        totalItems = len(filteredItems)

        navigation = []
        if page > 0:
            navigation += ["<P>rev Page"]
        if (page + 1) * pageSize < totalItems:
            navigation += ["<N>ext Page"]

        leave = ["<L>eave"] if sourceType == "Store" else ["<C>lose"]
        filterOption = [] if mode == "combat" else ["<F>ilter"]
        out = actions + navigation + filterOption + leave
        out = message + f"{style.RESET}\n" + ", ".join(out) + style.RESET
        options["message"] = ""
        return out

    @staticmethod
    def printInventory(source, options):
        page = options["currPage"]
        pageSize = options["pageSize"]
        filterValue = options["filter"]
        sourceType = type(source).__name__
 
        filterHeader = "" if filterValue == "all" else f" ({filterValue.title()})"
        if sourceType == "Player":
            print(f"{fore.CYAN}{style.BOLD}{source.name}'s Inventory{filterHeader}{style.RESET}")
            valueFactor = options["sellFactor"]
        elif sourceType == "Store":
            print(f"{fore.MAGENTA}{style.BOLD}Store Inventory{filterHeader}{style.RESET}")
            valueFactor = options["buyFactor"]

        filteredItems = source.items if filterValue == "all" else list(filter(lambda i: i.kind == filterValue, source.items))

        startIndex = pageSize * page
        s = slice(startIndex, startIndex + pageSize)
        pageItems = filteredItems[s]
        
        itemLines = []
        for i, item in enumerate(pageItems, 1):
            line = {
                "Name": f"{startIndex + i}) {item.displayName}",
                "ATK": f"{item.atk if item.atk else '--'}",
                "Type": f"{item.type}",
                "AC": f"{item.ac if item.ac else '--'}",
                "Value": f"{item.level * valueFactor}"
            }
            if sourceType == "Player":
                line["_color"] = fore.GREEN if item.equipped else style.RESET

            itemLines.append(line)

        Utils.printTable(["   Name", "ATK", "Type", "AC", "Value"], itemLines, [40, 8, 12, 8, 8])

    @staticmethod
    def getFilteredItem(source, options, index):
        filterValue = options["filter"]
 
        filteredItems = source.items if filterValue == "all" else list(filter(lambda i: i.kind == filterValue, source.items))

        try:
            return filteredItems[index]
        except IndexError:
            return None