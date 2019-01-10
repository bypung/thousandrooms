import random
from colorama import Fore, Back, Style

from item import Item
from utils import Utils
import item_list

class Store:
    def __init__(self, level):
        self.level = level
        self.items = []
        self.maxItems = 30
        self.generateItems()

    def generateItems(self):
        while len(self.items) < self.maxItems:
            newItem = Item(random.randint(max(self.level - 2, 1), self.level))
            if newItem.kind:
                self.items += [newItem]

    def addItem(self, item):
        self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)
