from colorama import Fore, Back, Style
from utils import Utils

class Creature:
    def __init__(self, info):
        for i in info:
            setattr(self, i, info[i])

        self.calculateDam()

    def calculateDam(self):
        self.dam = self.atk + (self.level * 2)

    def damage(self, value):
        self.hp -= value
        
    def heal(self, value = 0):
        if value == 0:
            self.hp = self.maxHp
        else :
            self.hp -= value