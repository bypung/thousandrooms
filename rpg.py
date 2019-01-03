import random
import os
import json

from colorama import init as coloramaInit
from colorama import Fore, Back, Style

from monster import Monster
from item import Item
from player import Player
from room import Room

class Game:
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.mode = "start"
        self.quit = False
        self.turn = 1
        self.nextLevel = 100
        self.level = 1
        self.options = {
            "start": "<L>oad, <N>ew",
            "combat": "<A>ttack, <D>efend, <R>un",
            "peace": "<R>est, <C>ontinue, <I>nventory, <S>ave",
            "gameOver": "<R>estart, <Q>uit",
            "inventory": "<E>quip, <C>lose"
        }
        self.resolver = {
            "start": self.startResolve,
            "combat": self.combatResolve,
            "peace": self.peaceResolve,
            "gameOver": self.gameOverResolve,
            "inventory": self.inventoryResolve
        }
        self.display = {
            "start": self.startDisplay,
            "combat": self.combatDisplay,
            "peace": self.peaceDisplay,
            "gameOver": self.gameOverDisplay,
            "inventory": self.inventoryDisplay
        }
        self.clearResolution()
        
        self.nextTurn()

    def rollDie(self, size):
        return random.randint(1, size)
    
    def incrementTurn(self, numTurns = 1):
        self.turn += numTurns
        if self.turn >= self.nextLevel:
            self.level += 1
            self.nextLevel += 100
            self.addResolution(f"{Fore.RED}The dungeon seems more dangerous...")
    
    def printRoll(self, roll, target):
        self.addResolution(f"[{roll} vs {target}]")
        
    def printStats(self):
        displayFunc = self.display[self.mode]
        displayFunc()

    def startDisplay(self):
        print(f"{Style.BRIGHT}Welcome To The Dungeon!\n")

    def combatDisplay(self):
        print(f"{Style.BRIGHT}Dungeon Level {self.level} - Turn {self.turn}\n")
        self.player.printStats()
        print("")
        self.monster.printStats()

    def peaceDisplay(self):
        print(f"{Style.BRIGHT}Dungeon Level {self.level} - Turn {self.turn}\n")
        self.player.printStats()

    def inventoryDisplay(self):
        self.player.printInventory()

    def gameOverDisplay(self):
        self.player.printStats()
        print("")
        self.monster.printStats()

    def printOptions(self):
        print(f"\n{Style.BRIGHT}{self.options[self.mode]}")

    def clearResolution(self):
        self.resolution = []

    def addResolution(self, text):
        self.resolution.append(text)

    def printResolution(self):
        if len(self.resolution) > 0:
            print("\n" + "\n".join(self.resolution))

    def playerAttack(self):
        atkRoll = self.rollDie(20) + self.player.atk
        
        monsterDefense = self.monster.ac
            
        if atkRoll >= monsterDefense:
            damRoll = self.rollDie(self.player.dam)
            self.addResolution(f"{Fore.GREEN}You hit for {damRoll}")
            self.monster.damage(damRoll)
            self.player.incrementHistory("dmg_done", damRoll)
        else:
            self.addResolution("You miss!")
        # self.printRoll(atkRoll, monsterDefense)
                
    def monsterAttack(self, playerDefending):
        atkRoll = self.rollDie(20) + self.monster.atk
        
        playerDefense = self.player.ac
        if playerDefending:
            playerDefense = playerDefense * 2

        if atkRoll >= playerDefense:
            damRoll = self.rollDie(self.monster.dam)
            self.addResolution(f"{Fore.RED}The {self.monster.name} {self.monster.getAtkVerb()} you for {Style.BRIGHT}{damRoll}")
            self.player.damage(damRoll)
            self.player.incrementHistory("dmg_taken", damRoll)
        else:
            self.addResolution(f"The {self.monster.name} misses!")
        # self.printRoll(atkRoll, playerDefense)

    def getReward(self, level):
        xp = self.monster.level * 100
        gp = self.monster.level * self.rollDie(10)
        self.player.xp += xp
        self.player.gp += gp
        self.addResolution(f"{Fore.YELLOW}You got {xp} XP and {gp} GP")
        
        levelUp = self.player.checkLevelUp()
        if levelUp:
            self.level += 1
            self.nextLevel = self.turn + 100
            self.addResolution(f"{Fore.YELLOW}You gained a level!")

        item = Item(self.monster.level)
        if item.type != "none":
            self.player.addItem(item)
            self.addResolution(f"{Fore.YELLOW}You found: {item.name}")
        
    def deathCheck(self):
        if self.player.hp <= 0:
            self.addResolution(f"{Fore.RED}{Style.BRIGHT}You die!")
            self.player.setEpitaph(self.monster, self.level)
            self.mode = "gameOver"

    def startResolve(self, action):
        if action == "L":            
            load = self.loadSave()
            self.player = Player(load["player"]["name"], load["player"])
            self.player.loadItems(load["items"])
            for i in load["game"]:
                setattr(self, i, load["game"][i])
            self.room = Room(self.player)
            self.monster = Monster(self.level)
            self.mode = "combat"
        elif action == "N":
            print("Choose a name:")
            name = input()
            self.player = Player(name)
            self.room = Room(self.player)
            self.monster = Monster(self.level)
            self.mode = "combat"
        else:
            return False
        return True

    def combatResolve(self, action):
        if action == "A":            
            self.playerAttack()
                
            if self.monster.hp <= 0:
                self.addResolution(f"The {self.monster.name} dies!")
                self.player.incrementHistory("kills")
                if self.player.hp <= self.player.maxHp * .25:
                    self.player.incrementHistory("risky_win")
                self.getReward(self.monster.level)
                self.mode = "peace"
            else:
                self.monsterAttack(False)  
                self.deathCheck()
            self.incrementTurn()
        elif action == "D":
            self.addResolution("You defend yourself!")

            self.monsterAttack(True)
            self.deathCheck()
            self.incrementTurn()
        elif action == "R":
            self.addResolution("You run away!")
            self.player.incrementHistory("run_away")
            self.mode = "peace"
            self.incrementTurn(10)
        else:
            return False
        return True

    def peaceResolve(self, action):
        if action == "C":
            self.addResolution("You continue your journey...")
            self.monster = Monster(self.level)
            self.mode = "combat"
        elif action == "R":
            timeToRest = (self.player.maxHp - self.player.hp) * 2
            self.addResolution("You take some time to recover...")
            self.player.heal()
            self.player.incrementHistory("rest")
            self.incrementTurn(timeToRest)
        elif action == "I":
            self.mode = "inventory"
        elif action == "S":
            self.createSave()
            print("<C>ontinue or <Q>uit?")
            choice = input()
            if len(choice) > 0 and choice[0].upper() == "Q":
                self.quit = True
        else:
            return False
        return True

    def gameOverResolve(self, action):
        if action == "R":
            print("restart")
            self.initialize()
        if action == "Q":
            self.quit = True
        return True

    def inventoryResolve(self, action):
        if action == "E":
            print("Which item do you wish to equip?")
            complete = False
            while not complete:
                itemNum = input()
                if itemNum == "":
                    complete = True
                else:
                    try:
                        i = int(itemNum) - 1
                        try:
                            item = self.player.items[i]
                            self.player.equipItem(i)
                            complete = True
                        except IndexError:
                            print("Invalid item number")
                    except ValueError:
                        #Handle the exception
                        print("Please enter an integer")
        if action == "C":
            self.mode = "peace"
        return True

    def takeInput(self):
        self.printOptions()
        resolved = False
        self.clearResolution()
        while not resolved:
            action = input()
            if len(action) > 0:
                action = action[0].upper()
                resolved = self.resolver[self.mode](action)
        
    def nextTurn(self):
        clear()
        self.printStats()
        self.printResolution()
        self.takeInput()

    def createSave(self):
        saveObj = {
            "player": dict(self.player.__dict__),
            "room": dict(self.room.__dict__),
            "game": {
                "turn": self.turn,
                "nextLevel": self.nextLevel,
                "level": self.level
            }
        }

        # make player items serializable
        saveObj["items"] = []
        for item in saveObj["player"]["items"]:
            saveObj["items"].append(item.__dict__)
        del saveObj["player"]["items"]

        # save the file
        with open('save.txt', 'w') as outfile:  
                json.dump(saveObj, outfile)

    def loadSave(self):
        with open('save.txt') as json_file:  
            return json.load(json_file)

clear=lambda: os.system('cls' if os.name == 'nt' else 'clear')
coloramaInit(autoreset=True)
game = Game()
while not game.quit:
    game.nextTurn()
clear()
game.player.printHistory()
