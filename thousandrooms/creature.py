from colored import fore, back, style

from .utils import Utils

class Creature:
    def __init__(self, info):
        for i in info:
            setattr(self, i, info[i])

        self.calculateDam()

    def calculateDam(self):
        return f"{style.DIM}({self.atk + 2}-{self.atk + (self.level * 2)}){style.RESET}"

    def damage(self, value, type):
        damage = value
        try:
            if type in self.resist:
                damage = value // 2
        except KeyError:
            pass
        except AttributeError:
            pass
        try:
            if self.vulnerability == type:
                damage = value * 2
        except KeyError:
            pass
        except AttributeError:
            pass
        self.hp -= damage
        return damage
        
    def heal(self, value = 0):
        if value == 0:
            self.hp = self.maxHp
        else :
            self.hp = min(self.hp + value, self.maxHp)