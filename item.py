import random
import item_list

class Item:
    def __init__(self, level):
        self.level = level
        self.equipped = False
        
        info = self.getItem(self.level)

        if info != None:
            for i in info:
                setattr(self, i, info[i])
        else:
            self.type = "none"

    @staticmethod
    def getItem(level):
        itemRoll = random.randint(1, 100) + (level * 5)
        itemType = "none"
        
        if itemRoll < 70:
            return None
        elif itemRoll < 90:
            itemType = "weapon"
        elif itemRoll < 100:
            itemType = "armor"
        else:
            itemType = "ring"
            
        items = item_list.items[itemType]
        
        qualityRoll = random.randint(1, 100) + (level * 5)

        quality = random.randint(0, level - 1)
        
        if qualityRoll >= 90:
            quality += 1
        
        return items[quality]