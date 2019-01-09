import random

from colorama import Fore, Back, Style

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
            info = self.getItem(self.level)
            if info != None:
                for i in info:
                    setattr(self, i, info[i])

                self.displayName = f"{self.name} of {self.ability}" if self.ability else self.name

                # improved items
                levelDiff = level - self.level
                if levelDiff > 0:
                    try:
                        descriptor = item_list.descriptors[self.kind][levelDiff]
                    except KeyError:
                        pass
                    try:
                        descriptor = item_list.descriptors[self.kind][self.type][levelDiff]
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

    @staticmethod
    def getItem(level):
        itemRoll = random.randint(level * 3, 100)
        itemType = "none"
        
        if itemRoll < 70:
            return None
        elif itemRoll < 85:
            itemType = "weapon"
        elif itemRoll < 95:
            itemType = "armor"
        else:
            itemType = "ring"
    
        items = [item for item in item_list.items if item["kind"] == itemType and item["level"] <= level and item["level"] > level - 5] 
        info = random.choice(items)
        return info

    @staticmethod
    def getOptions(source, options):
        page = options["currPage"]
        pageSize = options["pageSize"]
        filterValue = options["filter"]

        sourceType = type(source).__name__
        actions = []
        if sourceType == "Player":
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
        options = actions + navigation + ["<F>ilter"] + leave
        return ", ".join(options)

    @staticmethod
    def printInventory(source, options):
        page = options["currPage"]
        pageSize = options["pageSize"]
        filterValue = options["filter"]
        sourceType = type(source).__name__
 
        filterHeader = "" if filterValue == "all" else f" ({filterValue.title()})"
        if sourceType == "Player":
            print(f"{Fore.CYAN}{Style.BRIGHT}{source.name}'s Inventory{filterHeader}")
            valueFactor = 10
        elif sourceType == "Store":
            print(f"{Fore.MAGENTA}{Style.BRIGHT}Store Inventory{filterHeader}")
            valueFactor = 40

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
                line["_color"] = Fore.GREEN if item.equipped else Fore.WHITE

            itemLines.append(line)

        Utils.printTable(["   Name", "ATK", "Type", "AC", "Value"], itemLines, [30, 8, 12, 8, 8])

    @staticmethod
    def getFilteredItem(source, options, index):
        filterValue = options["filter"]
 
        filteredItems = source.items if filterValue == "all" else list(filter(lambda i: i.kind == filterValue, source.items))

        try:
            return filteredItems[index]
        except IndexError:
            return None