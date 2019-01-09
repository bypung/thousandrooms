import random
import item_list

class Item:
    def __init__(self, level, data = None):
        if level > 0:
            self.level = level
            self.equipped = False
            self.kind = ''
        
        info = data if data else self.getItem(self.level)

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