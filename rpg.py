import random
import math
import os
import json
import copy
from types import *

from colorama import init as coloramaInit
from colorama import Fore, Back, Style

from monster import Monster
from item import Item
from player import Player
from room import Room
from maps import Map
from door import Door
from store import Store
from utils import Utils

class Game:
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.mode = "start"
        self.quit = False
        self.turn = 1
        self.nextLevel = 100
        self.level = 1
        self.monster = None
        self.map = None
        self.store = None
        self.options = {
            "start": "<L>oad, <N>ew",
            "combat": "<A>ttack, <D>efend, <U>se Item, <R>un",
            "peace": "<R>est, <C>ontinue, <I>nventory, <M>erchant, <S>ave",
            "gameOver": "<R>estart, <Q>uit",
            "inventory": lambda : Item.getOptions(self.player, self.itemList) if self.player else "",
            "store": lambda : Item.getOptions(self.store, self.itemList) if self.store else "",
            "map": lambda : self.map.getOptions() if self.map else ""
        }
        self.resolver = {
            "start": self.startResolve,
            "combat": self.combatResolve,
            "peace": self.peaceResolve,
            "gameOver": self.gameOverResolve,
            "inventory": self.inventoryResolve,
            "store": self.storeResolve,
            "map": self.mapResolve
        }
        self.display = {
            "start": self.startDisplay,
            "combat": self.combatDisplay,
            "peace": self.peaceDisplay,
            "gameOver": self.gameOverDisplay,
            "inventory": self.inventoryDisplay,
            "store": self.storeDisplay,
            "map": self.mapDisplay
        }
        self.effectResolvers = {
            "healing": self.healingResolve,
            "time warp": self.timeWarpResolve,
            "shopping": self.shoppingResolve,
            "blinking": self.blinkingResolve,
            "fireball": self.fireballResolve
        }
        self.initItemList()
        self.clearResolution()
        self.nextTurn()

    def initItemList(self):
        self.itemList = {
            "currPage": 0,
            "pageSize": 15,
            "filter": "all",
            "mode": "peace"
        }

### NUMBER METHODS ###

    def rollDie(self, size):
        return random.randint(1, size)
    
    def incrementDungeonLevel(self):
        self.level += 1
        self.nextLevel += (100 * self.level)
        self.map.dungeonLevel = self.level

    def incrementTurn(self, numTurns = 1):
        self.turn += numTurns
        if self.turn >= self.nextLevel:
            self.incrementDungeonLevel()
            self.addResolution(f"{Fore.RED}The dungeon seems more dangerous...")
    
### PRINTING METHODS ###

    def printRoll(self, roll, target):
        self.addResolution(f"[{roll} vs {target}]")
        
    def printStats(self):
        displayFunc = self.display[self.mode]
        displayFunc()

    def clearResolution(self):
        self.resolution = []

    def addResolution(self, text):
        self.resolution.append(text)

    def printResolution(self):
        if len(self.resolution) > 0:
            print("\n" + "\n".join(self.resolution))

### DISPLAY METHODS ###

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
        print("")
        room = self.map.getCurrentRoom()
        room.printStats(self.map.getCurrentDoors())

    def inventoryDisplay(self):
        Item.printInventory(self.player, self.itemList)

    def storeDisplay(self):
        Item.printInventory(self.store, self.itemList)
        print(f"\n{Fore.YELLOW}GP: {self.player.gp}")

    def mapDisplay(self):
        self.map.printFloor(self.turn)

    def gameOverDisplay(self):
        self.player.printHistory()

    def printOptions(self):
        options = self.options[self.mode]
        if type(options) is LambdaType:
            options = options()
        print(f"\n{Style.BRIGHT}{options}")

### COMBAT METHODS ###

    def playerAttack(self):
        atkRoll = self.rollDie(20) + self.player.atk
        
        monsterDefense = self.monster.ac
            
        if atkRoll >= monsterDefense:
            damRoll = self.rollDie(self.player.dam)
            self.addResolution(f"{Fore.GREEN}You {self.player.getAtkVerb()} the {self.monster.name} for {damRoll}")
            damage = self.monster.damage(damRoll, self.player.atkType)
            if damage < damRoll:
                self.addResolution(f"{Fore.MAGENTA}Your weapon is not very effective.")
            if damage > damRoll:
                self.addResolution(f"{Fore.CYAN}Your weapon is very effective.")
            self.player.incrementHistory("dmg_done", damage)
        else:
            self.addResolution(f"{Fore.WHITE}You miss!")
        # self.printRoll(atkRoll, monsterDefense)
                
    def monsterAttack(self, playerDefending):
        atkRoll = self.rollDie(20) + self.monster.atk
        
        playerDefense = self.player.ac
        if playerDefending:
            playerDefense = playerDefense * 2

        if atkRoll >= playerDefense:
            damRoll = self.rollDie(self.monster.dam)
            self.addResolution(f"{Fore.RED}The {self.monster.name} {self.monster.getAtkVerb()} you for {Style.BRIGHT}{damRoll}")
            self.player.damage(damRoll, self.monster.atk_type)
            self.player.incrementHistory("dmg_taken", damRoll)
        else:
            self.addResolution(f"{Fore.WHITE}The {self.monster.name} misses!")
        # self.printRoll(atkRoll, playerDefense)

    def getReward(self, level):
        xp = self.monster.level * 100
        gp = self.monster.level * self.rollDie(10)
        self.player.xp += xp
        self.player.gp += gp
        self.addResolution(f"\n{Fore.YELLOW}You got {xp} XP and {gp} GP")
        
        levelUp = self.player.checkLevelUp()
        if levelUp:
            if self.level < self.player.level:
                self.incrementDungeonLevel()
            self.addResolution(f"{Fore.YELLOW}You gained a level!")

        item = Item(self.monster.level)
        if item.kind:
            self.player.addItem(item)
            self.addResolution(f"{Fore.YELLOW}You found: {item.displayName}")

    def monsterDeathCheck(self):
        if not self.monster:
            return
        if self.monster.hp <= 0:
            self.addResolution(f"{Fore.GREEN}The {self.monster.name} dies!")
            self.map.getCurrentRoom().removeMonster()
            self.player.incrementHistory("kills")
            if self.player.hp <= self.player.maxHp * .25:
                self.player.incrementHistory("risky_win")
            self.getReward(self.monster.level)
            self.monster = None
            self.mode = "peace"
        else:
            self.monsterAttack(False)  
            self.playerDeathCheck()
                
    def playerDeathCheck(self):
        if self.player.hp <= 0:
            self.addResolution(f"{Fore.RED}{Style.BRIGHT}You die!")
            self.player.killedBy(self.monster, self.level)
            self.mode = "gameOver"

### ITEM METHODS ###

    def resolveItem(self, item, mode):
        if mode == "combat" and item.type == "peace":
            return False
        if mode == "manage" and item.type == "combat":
            return False

        effect = item.effect
        escaped = False

        try:
            escaped = self.effectResolvers[effect]()
        except KeyError:
            pass

        if not escaped:
            self.monsterDeathCheck()

        self.mode = "combat" if self.monster else "peace"
        self.incrementTurn()
        return True

    def healingResolve(self):
        self.player.heal(self.player.maxHp // 2)
        self.addResolution(f"{Fore.GREEN}You feel much better!")
        return False

    def timeWarpResolve(self):
        self.level -= 1
        self.nextLevel += self.level * 100
        self.addResolution(f"{Fore.GREEN}The dungeon feels less dangerous...")
        return False

    def shoppingResolve(self):
        self.initItemList()
        self.itemList["mode"] = "buy"
        self.mode = "store"
        bonus = self.player.level * 10
        self.player.gp += bonus
        self.addResolution(f"{Fore.YELLOW}You are transported to the store with an extra {bonus} GP!")
        return False

    def blinkingResolve(self):
        pp = self.map.playerPosition
        minR = max(0, pp[1] - 2)
        maxR = min(self.map.width - 1, pp[1] + 2)
        minC = max(0, pp[2] - 2)
        maxC = min(self.map.width - 1, pp[2] + 2)
        newPos = (random.randint(minR, maxR), random.randint(minC, maxC))
        while newPos == (pp[1], pp[2]):
            newPos = (random.randint(minR, maxR), random.randint(minC, maxC))
        self.map.setPlayerPosition(pp[0], newPos[0]. newPos[1])
        self.addResolution(f"{Fore.MAGENTA}You are transported to another room!")
        newRoom = self.map.getCurrentRoom()
        newRoom.generateContents()
        self.monster = newRoom.monster
        if self.monster:
            self.mode = "combat"
            return False
        else:
            self.mode = "peace"
            return True

    def fireballResolve(self):
        dam = 0
        for i in range(self.player.level):
            dam += self.rollDie(8)
        if self.monster.resist == "fire":
            dam = dam // 2
        if self.monster.vulnerability == "fire":
            dam = dam * 2
        self.monster.damage(dam)
        self.addResolution(f"{Fore.GREEN}The {self.monster.displayName} is blasted for {dam}!")
        return False

### RESOLUTION METHODS ###

    def mapResolve(self, action):
        if action == "B":
            self.mode = "peace"
        elif action in ["N", "S", "E", "W", "U", "D"]:
            direction = action.lower()
            for key, door in self.map.getCurrentDoors():
                if key[0] == direction and door.exists:
                    if direction == "u" and self.map.playerPosition[0] == 0:
                        print(f"{Fore.MAGENTA}{Style.BRIGHT}Are you sure you want to exit the dungeon? <Y>es or <N>o")
                        choice = input()
                        if choice.lower() == "y":
                            self.mode = "gameOver"
                            self.player.setEpitaph("Escaped the dungeon!")
                            return True
                    else:
                        self.map.movePlayer(direction)
                        door.useDoor()
                        if 'traveling' in self.player.abilities:
                            travelRoll = self.rollDie(10)
                            if travelRoll > self.player.getAbilityLevel('traveling'):
                                self.incrementTurn()
                        else:
                            self.incrementTurn()
                        monster = self.map.getCurrentRoom().monster
                        if monster != None:
                            self.monster = monster
                            self.mode = "combat"
        else:
            return False
        return True

    def startResolve(self, action):
        if action == "L":            
            load = self.loadSave()
        elif action == "N":
            print("Choose a name:")
            name = input()
            self.player = Player(name)
            self.map = Map()
        else:
            return False
        self.mode = "peace"
        return True

    def combatResolve(self, action):
        if action == "A":            
            self.playerAttack()      
            self.monsterDeathCheck()
            self.incrementTurn()
        elif action == "D":
            self.addResolution("You defend yourself!")
            self.monsterAttack(True)
            self.playerDeathCheck()
            self.incrementTurn()
        elif action == "U":
            self.mode = "inventory"
            self.initItemList()
            self.itemList["filter"] = "usable"
            self.itemList["mode"] = "combat"
        elif action == "R":
            self.player.incrementHistory("run_away")
            exits = self.map.getCurrentDoors()
            escaped = False
            while not escaped:
                door = random.choice(exits)
                if (door[1].used):
                    self.map.movePlayer(door[0])
                    escaped = True
            self.mode = "peace"
            if 'running' in self.player.abilities:
                self.incrementTurn(10 - self.player.getAbilityLevel('running'))
                self.addResolution(f"{Fore.GREEN}You run away very quickly!")
            else:
                self.incrementTurn(10)
                self.addResolution("You run away!")
        else:
            return False
        return True

    def peaceResolve(self, action):
        if action == "C":
            self.mode = "map"
        elif action == "R":
            self.addResolution("You take some time to recover...")
            restFactor = math.sqrt(self.player.level)
            if 'regeneration' in self.player.abilities:
                restFactor -= 0.2 * self.player.getAbilityLevel('regeneration')
                self.addResolution(f"{Fore.GREEN}You heal quickly...")
            timeToRest = math.floor((self.player.maxHp - self.player.hp) * restFactor)
            self.player.heal()
            self.player.incrementHistory("rest")
            self.incrementTurn(timeToRest)
        elif action == "I":
            self.initItemList()
            self.mode = "inventory"
        elif action == "M":
            self.initItemList()
            self.itemList["mode"] = "buy"
            self.store = Store(self.level)
            self.mode = "store"
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

    def filterItems(self):
        print("Filter: <W>eapons, <A>rmor, <R>ings, <U>sable, <E>verything")
        choice = input()
        filterValue = "all"
        if choice.lower() == "w":
            filterValue = "weapon"
        if choice.lower() == "a":
            filterValue = "armor"
        if choice.lower() == "r":
            filterValue = "ring"
        if choice.lower() == "u":
            filterValue = "usable"
        self.itemList["currPage"] = 0
        self.itemList["filter"] = filterValue

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
                            item = Item.getFilteredItem(self.player, self.itemList, i)
                            if item:
                                self.player.equipItem(item)
                                complete = True
                        except IndexError:
                            print("Invalid item number")
                    except ValueError:
                        #Handle the exception
                        print("Please enter an integer")
        if action == "P":
            self.itemList["currPage"] -= 1
        if action == "N":
            self.itemList["currPage"] += 1
        if action == "F":
            self.filterItems()
        if action == "U":
            print("Use which item?")
            complete = False
            while not complete:
                itemNum = input()
                if itemNum == "":
                    complete = True
                else:
                    try:
                        i = int(itemNum) - 1
                        try:
                            item = Item.getFilteredItem(self.player, self.itemList, i)
                            used = self.resolveItem(item, self.itemList["mode"])
                            if used:
                                self.player.removeItem(item)
                            complete = True
                        except IndexError:
                            print("Invalid item number")
                    except ValueError:
                        #Handle the exception
                        print("Please enter an integer")
        if action == "C":
            self.mode = "peace"
        return True

    def storeResolve(self, action):
        if action == "B":
            print("Which item do you wish to buy?")
            complete = False
            while not complete:
                itemNum = input()
                if itemNum == "":
                    complete = True
                else:
                    try:
                        i = int(itemNum) - 1
                        try:
                            item = Item.getFilteredItem(self.store, self.itemList, i)
                            self.player.addItem(item)
                            complete = True
                        except IndexError:
                            print("Invalid item number")
                    except ValueError:
                        #Handle the exception
                        print("Please enter an integer")
        if action == "S":
            print("sell")
        if action == "P":
            self.itemList["currPage"] -= 1
        if action == "N":
            self.itemList["currPage"] += 1
        if action == "F":
            self.filterItems()
        if action == "L":
            self.mode = "peace"
        return True

### LIFECYCLE METHODS ###

    def takeInput(self):
        self.printOptions()
        resolved = False
        self.clearResolution()
        action = input()
        if len(action) > 0:
            action = action[0].upper()
            self.resolver[self.mode](action)
        
    def nextTurn(self):
        clear()
        self.printStats()
        self.printResolution()
        self.takeInput()

    def createSave(self):
        saveObj = {
            "player": dict(copy.deepcopy(self.player).__dict__),
            "map": dict(copy.deepcopy(self.map).__dict__),
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

        # make map rooms serializable
        saveObj["map"]["rooms"] = {}
        saveObj["map"]["monsters"] = {}
        saveObj["map"]["doors"] = {
            "ns": {},
            "ew": {}
        }
        saveObj["map"]["stairs"] = {}

        for f, floor in enumerate(saveObj["map"]["floors"]):
            for r in range(self.map.width):
                for c in range(self.map.width):
                    saveKey = f"{f}-{r}-{c}"
                    roomDict = floor["rooms"][(r,c)].__dict__
                    monster = roomDict["monster"]
                    saveObj["map"]["monsters"][saveKey] = monster.__dict__ if monster != None else None
                    del roomDict["monster"]
                    saveObj["map"]["rooms"][saveKey] = roomDict
                    try: 
                        ns = floor["doors"]["ns"][(r,c)].__dict__
                        saveObj["map"]["doors"]["ns"][saveKey] = ns
                    except KeyError:
                        pass
                    try:
                        ew = floor["doors"]["ew"][(r,c)].__dict__
                        saveObj["map"]["doors"]["ew"][saveKey] = ew
                    except KeyError:
                        pass
                    try:
                        stairs = floor["stairs"][(r,c)].__dict__
                        saveObj["map"]["stairs"][saveKey] = stairs
                    except KeyError:
                        pass

        del saveObj["map"]["floors"]

        # save the file
        with open('save.json', 'w') as outfile:  
                json.dump(saveObj, outfile)

    def loadSave(self):
        with open('save.json') as json_file:  
            load = json.load(json_file)
            self.player = Player(load["player"]["name"], load["player"])
            self.player.loadItems(load["items"])
            for i in load["game"]:
                setattr(self, i, load["game"][i])
            self.map = Map(load["map"]["numFloors"], load["map"]["width"], load["map"])


clear=lambda: os.system('cls' if os.name == 'nt' else 'clear')
coloramaInit(autoreset=True)
game = Game()
while not game.quit:
    game.nextTurn()
clear()
