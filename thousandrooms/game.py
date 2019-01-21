import random
import math
import os
import json
import copy
import sys
import time
from types import *

from colored import fore, back, style

from .monster import Monster
from .item import Item
from .player import Player
from .room import Room
from .maps import Map
from .door import Door
from .store import Store
from .utils import Utils

clear=lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Game:
    saveFilePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "save")
    saveListFilePath = os.path.join(saveFilePath, "saveList.json")
    playerQuit = False
    restart = False

    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self.mode = "peace"
        self.restart = False

        self.turn = 1
        self.nextLevel = 100
        self.level = 1
        self.ironman = False
        self.saveId = ""

        self.player = None
        self.monster = None
        self.map = None
        self.store = None

        self.options = {
            "combat": "\n<A>ttack, <D>efend, <X>amine, <U>se Item, <R>un",
            "peace": "\n<R>est, <C>ontinue, <I>nventory, <M>erchant, <S>ave, <Q>uit",
            "gameOver": "\n<R>estart, <Q>uit",
            "inventory": lambda : Item.getOptions(self.player, self.itemListOptions) if self.player else "",
            "store": lambda : Item.getOptions(self.store, self.itemListOptions) if self.store else "",
            "map": lambda : self.map.getOptions() if self.map else ""
        }
        self.resolver = {
            "combat": self.combatResolve,
            "peace": self.peaceResolve,
            "gameOver": self.gameOverResolve,
            "inventory": self.inventoryResolve,
            "store": self.storeResolve,
            "map": self.mapResolve
        }
        self.display = {
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
            "fireball": self.fireballResolve,
            "digging": self.diggingResolve,
            "teleport": self.teleportResolve,
            "invisibility": self.invisibilityResolve,
            "knowledge": self.knowledgeResolve
        }
        self.inititemListOptions()
        self.clearResolution()

    def inititemListOptions(self):
        self.itemListOptions = {
            "currPage": 0,
            "pageSize": 15,
            "filter": "all",
            "mode": "peace",
            "sellFactor": 20,
            "buyFactor": 100,
            "message": "",
            "gp": 0
        }

### NUMBER METHODS ###

    def rollDie(self, size):
        return random.randint(1, size)
    
    def rollDamage(self, creature):
        return self.rollDie(creature.level) + self.rollDie(creature.level) + self.rollDie(creature.atk)
    
    def incrementDungeonLevel(self):
        self.level += 1
        self.nextLevel = self.turn + (100 * self.level)
        self.map.dungeonLevel = self.level

    def incrementTurn(self, numTurns = 1):
        self.turn += numTurns
        if self.turn >= self.nextLevel:
            self.incrementDungeonLevel()
            self.addResolution(f"{fore.RED}The dungeon seems more dangerous...")
    
### PRINTING METHODS ###

    def printRoll(self, roll, target):
        self.addResolution(f"[{roll} vs {target}]")
        
    def printStats(self):
        displayFunc = self.display[self.mode]
        displayFunc()

    def printStatHeader(self):
        print(f"{style.BOLD}Dungeon Level {self.map.playerPosition[0] + 1} - Turn {self.turn}{style.DIM}/{self.nextLevel}\n{style.RESET}")

    def clearResolution(self):
        self.resolution = []

    def addResolution(self, text):
        self.resolution.append(text)

    def printResolution(self):
        if len(self.resolution) > 0:
            print("\n" + f"{style.RESET}\n".join(self.resolution) + style.RESET)

### DISPLAY METHODS ###

    def combatDisplay(self):
        self.printStatHeader()
        self.player.printStats()
        print("")
        self.monster.printStats(self.player.monsterLore)

    def peaceDisplay(self):
        self.printStatHeader()
        self.player.printStats()
        print("")
        room = self.map.getCurrentRoom()
        room.printStats(self.map.getCurrentDoors())

    def inventoryDisplay(self):
        Item.printInventory(self.player, self.itemListOptions)

    def storeDisplay(self):
        invSource = self.store if self.itemListOptions["mode"] == "buy" else self.player
        self.itemListOptions["gp"] = self.player.gp
        Item.printInventory(invSource, self.itemListOptions)

    def mapDisplay(self):
        self.map.printFloor(self.turn, self.nextLevel)

    def gameOverDisplay(self):
        self.player.printHistory(self.turn)

    def printOptions(self):
        options = self.options[self.mode]
        if type(options) is LambdaType:
            options = options()
        print(f"{style.BOLD}{options}")

### COMBAT METHODS ###

    def playerAttack(self):
        if self.monster.charges > 0:
            self.player.incrementHistory("reckless")

        atkRoll = self.rollDie(20) + self.player.atk
        
        monsterDefense = self.monster.ac
            
        if atkRoll == 20 or atkRoll >= monsterDefense:
            damRoll = self.rollDamage(self.player)
            damage = self.monster.damage(damRoll, self.player.atkType)
            self.addResolution(f"{fore.GREEN}You {self.player.getAtkVerb()} the {self.monster.name} for {damage}")
            if damage < damRoll:
                self.addResolution(f"{fore.MAGENTA}Your weapon is not very effective.")
                self.addLore("resist")
            if damage > damRoll:
                self.addResolution(f"{fore.CYAN}Your weapon is very effective.")
                self.addLore("vulnerability")
            self.player.incrementHistory("dmg_done", damage)
        else:
            self.addResolution(f"{fore.WHITE}You miss!")
                
    def monsterAttack(self, playerDefending):
        if self.monster.quotes:
            quoteRoll = self.rollDie(3)
            if quoteRoll == 1:
                self.addResolution(f"{fore.LIGHT_SLATE_BLUE}{random.choice(self.monster.quotes)}")

        if self.monster.charges == 0:
            chargeRoll = self.rollDie(10)
            if chargeRoll == 1:
                self.monster.charges += self.monster.chargeRate
                self.addResolution(f"{fore.DARK_ORANGE_3B}The {self.monster.name} readies an attack...")
                return

        atkRoll = self.rollDie(20) + self.monster.atk
        
        playerDefense = self.player.ac
        if playerDefending:
            playerDefense = playerDefense * 2 - 10

        if atkRoll == 20 or atkRoll >= playerDefense:
            damRoll = self.rollDamage(self.monster)
            self.addResolution(f"{fore.RED}The {self.monster.name} {self.monster.getAtkVerb()} you for {style.BOLD}{damRoll}")
            self.player.damage(damRoll, self.monster.atk_type)
            self.player.incrementHistory("dmg_taken", damRoll)
        else:
            self.addResolution(f"{fore.WHITE}The {self.monster.name} misses!")

        while self.monster.charges > 0:
            self.monster.charges -= 1
            specAtkRoll = self.rollDie(20) + self.monster.atk
            if not self.monster.special:
                specAtkRoll += int(math.sqrt(self.monster.level))
            if specAtkRoll >= playerDefense:
                self.addLore("special")
                if self.monster.special == "drain":
                    self.player.drain(random.randint(1, self.monster.level) * 50)
                    self.addResolution(f"{fore.PALE_TURQUOISE_1}It drains your life essence!")
                elif self.monster.special == "melt":
                    if "acid" in self.player.resist:
                        self.addResolution(f"{fore.GREEN}You resist the spray of acid!")
                    else:
                        meltables = [item for item in self.player.items if item.kind == "weapon" or item.type == "metal"]
                        if len(meltables) > 0:
                            item = random.choice(meltables)
                            self.addResolution(f"{fore.CHARTREUSE_1}It melts your {item.displayName} with acid!")
                            self.player.removeItem(item)
                elif self.monster.special == "burn":
                    if "fire" in self.player.resist:
                        self.addResolution(f"{fore.GREEN}You resist the burst of flame!")
                    else:
                        burnables = [item for item in self.player.items if item.name == "Scroll" or item.type in ["cloth", "leather"]]
                        if len(burnables) > 0:
                            item = random.choice(burnables)
                            self.addResolution(f"{fore.CHARTREUSE_1}It burns your {item.displayName} to ash!")
                            self.player.removeItem(item)
                elif self.monster.special == "freeze":
                    if "cold" in self.player.resist:
                        self.addResolution(f"{fore.GREEN}You resist the blast of frost!")
                    else:
                        freezables = [item for item in self.player.items if item.name == "Potion"]
                        if len(freezables) > 0:
                            item = random.choice(freezables)
                            self.addResolution(f"{fore.CHARTREUSE_1}It freezes your {item.displayName} and shatters it!")
                            self.player.removeItem(item)
                elif self.monster.special == "shock":
                    if "electric" in self.player.resist:
                        self.addResolution(f"{fore.GREEN}You resist the bolt of lightning!")
                    else:
                        self.addResolution(f"{fore.CHARTREUSE_1}It shocks you and makes you drop your weapon!")
                        self.player.unequipItem("weapon")
                elif self.monster.special == "sunder":
                    sunderables = [item for item in self.player.items if item.kind in ["weapon", "armor"] and item.equipped]
                    item = random.choice(sunderables)
                    if item:
                        self.addResolution(f"{fore.CHARTREUSE_1}It strikes your {item.displayName} and damages it!")
                        if item.kind == "weapon":
                            item.atk -= 1
                            if item.atk == 0:
                                self.player.removeItem(item)
                                self.addResolution(f"{fore.CHARTREUSE_1}Your weapon is destroyed!")
                        else:
                            item.ac -= 1
                            if item.ac == 0:
                                self.player.removeItem(item)
                                self.addResolution(f"{fore.CHARTREUSE_1}Your armor is destroyed!")
                        self.player.applyItems()

                else:
                    damRoll = self.rollDamage(self.monster)
                    self.addResolution(f"{fore.RED}The {self.monster.name} {self.monster.getAtkVerb()} you for {style.BOLD}{damRoll}")
                    self.player.damage(damRoll, self.monster.atk_type)
                    self.player.incrementHistory("dmg_taken", damRoll)
            else:
                self.addResolution(f"{fore.WHITE}Its special attack fails!")      
        self.playerDeathCheck()

    def getReward(self, level):
        xp = self.monster.level * 50
        gp = self.monster.level * self.rollDie(10)
        self.player.xp += xp
        self.player.gp += gp
        self.addResolution(f"\n{fore.YELLOW}You got {xp} XP and {gp} GP")
        self.checkPlayerLevelUp()
        
        item = Item(self.monster.level, None, ["weapon", "armor", "ring"] if self.monster.isBoss else [])
        if item.kind:
            self.player.addItem(item)
            self.addResolution(f"{fore.YELLOW}You found: {item.displayName}")

    def checkPlayerLevelUp(self):
        levelUp = self.player.checkLevelUp()
        if levelUp:
            if self.level < self.player.level:
                self.incrementDungeonLevel()
            self.addResolution(f"{fore.YELLOW}You gained a level!")

    def monsterDeathCheck(self):
        if not self.monster:
            return
        if self.monster.hp <= 0:
            self.addResolution(f"{fore.GREEN}The {self.monster.name} dies!")
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
            self.addResolution(f"{fore.RED}{style.BOLD}You die!")
            self.player.killedBy(self.monster, self.map.playerPosition[0] + 1)
            self.mode = "gameOver"

    def playerEscape(self):
        self.monster.charges = 0
        self.monster = None
        exits = [e for e in self.map.getCurrentDoors() if e[1].used]
        if len(exits) == 0:
            exits = self.map.getCurrentDoors()
        door = random.choice(exits)
        self.map.movePlayer(door[0])
        newRoom = self.map.getCurrentRoom()
        self.monster = newRoom.monster
        self.mode = "combat" if self.monster else "peace"

    def addLore(self, area = None):
        id = str(self.monster.id)
        try:
            lore = self.player.monsterLore[id]
        except KeyError:
            lore = { "resist": False, "vulnerability": False, "special": False}
            self.player.monsterLore[id] = lore
            
        learned = False
        if not area:
            unknowns = [key for key, value in lore.items() if value == False]
            if len(unknowns) == 0:
                self.addResolution("There is nothing more for you to learn!")
                return
            else:
                area = random.choice(unknowns)
                learned = True
        
        if not lore[area]:
            learned = True
            lore[area] = True
            self.addResolution(f"{fore.DEEP_PINK_3B}You gain new knowledge!")

        if learned:
            if lore["resist"] and lore["vulnerability"] and lore["special"]:
                xp = self.monster.level * 50
                self.player.xp += xp
                self.addResolution(f"{fore.YELLOW}You gained {xp} XP for mastering your knowledge of this creature!")        
                self.checkPlayerLevelUp()

### ITEM METHODS ###

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
        self.itemListOptions["currPage"] = 0
        self.itemListOptions["filter"] = filterValue

    def selectItem(self, source, prompt):
        sys.stdout.write(f"{prompt} {style.DIM}<Enter> to cancel {style.RESET}")
        complete = False
        while not complete:
            itemNum = input()
            if itemNum == "":
                return None
            else:
                try:
                    i = int(itemNum) - 1
                    try:
                        item = Item.getFilteredItem(source, self.itemListOptions, i)
                        complete = True
                        return item
                    except IndexError:
                        print("Invalid item number")
                except ValueError:
                    #Handle the exception
                    print("Please enter an integer")

    def getItemPrice(self, item, action):
        factor = self.itemListOptions["buyFactor" if action == "buy" else "sellFactor"]
        price = item.level * self.itemListOptions["buyFactor"]
        if item.kind == "usable":
            price = price * 2
        return price

    def resolveItem(self, item, mode):
        if item.kind != "usable":
            return False
        if mode == "combat" and item.type == "peace":
            return False
        if mode == "peace" and item.type == "combat":
            return False

        effect = item.effect
        escaped = False

        try:
            used = self.effectResolvers[effect]()
        except KeyError:
            pass

        if used:
            if self.monster:
                self.mode = "combat"
                self.monsterDeathCheck()
            elif self.mode != "store": 
                self.mode = "peace"
            self.incrementTurn()
        return used

    def healingResolve(self):
        self.player.heal(self.player.maxHp // 2)
        self.addResolution(f"{fore.GREEN}You feel much better!")
        return True

    def timeWarpResolve(self):
        self.nextLevel += self.level * 50
        self.addResolution(f"{fore.GREEN}The dungeon feels less dangerous...")
        return True

    def invisibilityResolve(self):
        self.playerEscape()
        self.addResolution(f"{fore.CYAN}You turn invisible and sneak away!")
        return True

    def knowledgeResolve(self):
        self.map.discoverStairs()
        self.nextLevel -= self.level * 25
        self.addResolution(f"{fore.CYAN}The secrets of the dungeon become clearer!")
        self.addResolution(f"{fore.DARK_ORANGE_3B}The monsters sense your questing mind...")
        if self.turn >= self.nextLevel:
            self.incrementDungeonLevel()
        return True

    def teleportResolve(self):
        pp = self.map.playerPosition
        prompt = "Teleport which direction?"
        validDirs = []
        if pp[1] > 0:
            validDirs += "n"
            prompt += " <N>orth"
        if pp[1] < self.map.width - 1:
            validDirs += "s"
            prompt += " <S>outh"
        if pp[2] < self.map.width - 1:
            validDirs += "e"
            prompt += " <E>ast"
        if pp[2] > 0:
            validDirs += "w"
            prompt += " <W>est"
        prompt += f"{style.DIM} <Enter> to cancel {style.RESET}"
        sys.stdout.write(prompt)
        choice = input()
        if choice and choice in validDirs:
            teleport = {
                "n": lambda: self.map.setPlayerPosition(pp[0], random.randint(0, pp[1] - 1), pp[2]),
                "s": lambda: self.map.setPlayerPosition(pp[0], random.randint(pp[1] + 1, self.map.width - 1), pp[2]),
                "e": lambda: self.map.setPlayerPosition(pp[0], pp[1], random.randint(pp[2] + 1, self.map.width - 1)),
                "w": lambda: self.map.setPlayerPosition(pp[0], pp[1], random.randint(0, pp[2] - 1))
            }
            teleport[choice]()
            self.addResolution(f"{fore.CYAN}You are magically transported!")
            newRoom = self.map.getCurrentRoom()
            newRoom.generateContents(self.level)
            self.monster = newRoom.monster
            if self.monster:
                self.mode = "combat"
            else:
                self.mode = "peace"
            return True
        else: 
            return False

    def shoppingResolve(self):
        self.inititemListOptions()
        self.itemListOptions["mode"] = "buy"
        self.store = Store(self.level)
        self.mode = "store"
        bonus = self.player.level * 10
        self.player.gp += bonus
        self.itemListOptions["message"] = f"{fore.YELLOW}You are transported to the store with an extra {bonus} GP!"
        return True

    def blinkingResolve(self):
        pp = self.map.playerPosition
        minR = max(0, pp[1] - 2)
        maxR = min(self.map.width - 1, pp[1] + 2)
        minC = max(0, pp[2] - 2)
        maxC = min(self.map.width - 1, pp[2] + 2)
        newPos = (random.randint(minR, maxR), random.randint(minC, maxC))
        while newPos == (pp[1], pp[2]):
            newPos = (random.randint(minR, maxR), random.randint(minC, maxC))
        self.map.setPlayerPosition(pp[0], newPos[0], newPos[1])
        self.addResolution(f"{fore.MAGENTA}You are transported to another room!")
        newRoom = self.map.getCurrentRoom()
        newRoom.generateContents(self.level)
        self.monster = newRoom.monster
        if self.monster:
            self.mode = "combat"
        else:
            self.mode = "peace"
        return True

    def diggingResolve(self):
        room = self.map.getCurrentRoom()
        doors = [door for door in self.map.getCurrentDoors() if not door[1].exists]

        if len(doors) == 0:
            self.itemListOptions["message"] = f"{fore.ORANGE}There's nowhere to dig!"
            return False

        prompt = "Dig which direction?"
        for (doorDir, door) in doors:
            if doorDir == "n":
                prompt += " <N>orth"
            elif doorDir == "s":
                prompt += " <S>outh"
            elif doorDir == "e":
                prompt += " <E>ast"
            elif doorDir == "w":
                prompt += " <W>est"
        prompt += f"{style.DIM} <Enter> to cancel {style.RESET}"
        sys.stdout.write(prompt)
        choice = input()
        if choice == "":
            return False
        choice = choice[0].lower()
        for (doorDir, door) in doors:
            if choice == doorDir:
                door.exists = True
                self.mode = "peace"
                self.addResolution(f"{fore.DARK_ORANGE_3B}You dug a new door!")
                return True
        return False
             

    def fireballResolve(self):
        dam = 0
        for i in range(self.player.level):
            dam += self.rollDie(8)
        if self.monster.resist == "fire":
            dam = dam // 2
        if self.monster.vulnerability == "fire":
            dam = dam * 2
        self.monster.damage(dam, "fire")
        self.addResolution(f"{fore.GREEN}The {self.monster.name} is blasted for {dam}!")
        return True

### RESOLUTION METHODS ###

    def mapResolve(self, action):
        if action == "B" or action == "":
            self.mode = "peace"
        elif action in ["N", "S", "E", "W", "U", "D"]:
            direction = action.lower()
            for key, door in self.map.getCurrentDoors():
                if key[0] == direction and door.isValid():
                    if direction == "u" and self.map.playerPosition[0] == 0:
                        print(f"{fore.MAGENTA}{style.BOLD}Are you sure you want to exit the dungeon? <Y>es or <N>o{style.RESET}")
                        choice = input()
                        if choice.lower() == "y":
                            self.mode = "gameOver"
                            epitaph = "Defeated the dungeon!" if self.player.hasIdol else "Fled the dungeon!"
                            self.player.setEpitaph(epitaph)
                            return True
                    elif direction == "d" and self.map.playerPosition[0] == self.map.numFloors - 1:
                        self.addResolution(f"{fore.YELLOW}{style.BOLD}You found the Idol of Onekrum!")
                        self.player.hasIdol = True
                        self.addResolution(f"{fore.RED}{style.BOLD}Enraged monsters fill the dungeon...")
                        self.map.resetRooms()
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
        elif action == "L":            
            loreRating = self.player.getLoreRating(self.map.playerPosition[0])
            rooms = self.map.getConnectedRooms()
            success = False
            for room in rooms:
                if room.monster and not room.monster.known:
                    loreRoll = self.rollDie(100)
                    checkNum = loreRating * 3 if self.player.hasSeenMonster(room.monster) else loreRating
                    if (loreRoll <= checkNum):
                        success = True
                        room.monster.known = True
            if success:
                self.map.message = f"{fore.GREEN}You hear something nearby!"
            else:
                self.map.message = f"{fore.CYAN}You listen carefully but don't hear anything new..."
            self.incrementTurn(3)
        else:
            return False
        return True

    def combatResolve(self, action):
        if action == "A":            
            self.playerAttack()      
            self.monsterDeathCheck()
            self.incrementTurn()
        elif action == "D":
            self.addResolution("You defend yourself!")
            self.monsterAttack(True)
            self.incrementTurn()
        elif action == "X":
            self.addResolution("You study your opponent...")
            self.addLore()
            self.monsterAttack(True)
            self.incrementTurn()
        elif action == "U":
            self.mode = "inventory"
            self.inititemListOptions()
            self.itemListOptions["filter"] = "usable"
            self.itemListOptions["mode"] = "combat"
        elif action == "R":
            self.monster.heal(math.floor(self.monster.hd * self.monster.level / (4 + self.player.getAbilityLevel('running') * .075)))
            self.player.incrementHistory("run_away")
            self.playerEscape()
            if 'running' in self.player.abilities:
                self.incrementTurn(10 - self.player.getAbilityLevel('running'))
                self.addResolution(f"{fore.GREEN}You run away very quickly!")
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
                restFactor -= 0.075 * self.player.getAbilityLevel('regeneration')
                self.addResolution(f"{fore.GREEN}You heal quickly...")
            timeToRest = math.floor((self.player.maxHp - self.player.hp) * restFactor)
            self.player.heal()
            self.player.incrementHistory("rest")
            self.incrementTurn(timeToRest)
        elif action == "I":
            self.inititemListOptions()
            self.mode = "inventory"
        elif action == "M":
            if self.player.hasIdol:
                self.addResolution(f"{fore.RED}It's too dangerous to go to the store!")
                return True
            self.inititemListOptions()
            self.itemListOptions["mode"] = "buy"
            self.store = Store(self.level)
            self.mode = "store"
            timeToShop = (self.map.playerPosition[0] + 1) * (10 - self.player.getAbilityLevel('traveling'))
            self.itemListOptions["message"] = f"{style.DIM}This trip will take {timeToShop} turns..."
            self.incrementTurn(timeToShop)
        elif action == "S":
            self.createSave()
            print("<C>ontinue or <Q>uit?")
            choice = input()
            if len(choice) > 0 and choice[0].upper() == "Q":
                self.endGame()
        elif action == "Q":
            if not self.saveId:
                print(f"{fore.RED}Quit without saving? {style.DIM}<Y>es or <N>o{style.RESET}")
                choice = input()
                if len(choice) > 0 and choice[0].upper() == "Y":
                    self.endGame()
            else:
                self.endGame()
        else:
            return False
            
        return True

    def gameOverResolve(self, action):
        if action == "R":
            self.restart = True
        elif action == "Q":
            self.endGame()
        return True

    def inventoryResolve(self, action):
        if action == "E":
            item = self.selectItem(self.player, "Which item do you wish to equip?")
            if item:
                self.player.equipItem(item)
        elif action == "P":
            self.itemListOptions["currPage"] -= 1
        elif action == "N":
            self.itemListOptions["currPage"] += 1
        elif action == "F":
            self.filterItems()
        elif action == "U":
            self.itemListOptions["currPage"] = 0
            self.itemListOptions["filter"] = "usable"
            clear()
            self.inventoryDisplay()
            item = self.selectItem(self.player, "\nUse which item?")
            if item:
                used = self.resolveItem(item, self.itemListOptions["mode"])
                if used:
                    self.player.removeItem(item)
        elif action == "C" or action == "":
            self.mode = self.itemListOptions["mode"]
        return True

    def storeResolve(self, action):
        if action == "B":
            if self.itemListOptions["mode"] == "sell":
                self.itemListOptions["mode"] = "buy"
            else:
                item = self.selectItem(self.store, "Which item do you wish to buy?")
                if item:
                    price = self.getItemPrice(item, "buy")
                    if price <= self.player.gp:
                        self.player.incrementHistory("buy_item")
                        self.itemListOptions["message"] = f"{fore.CYAN}You bought the {item.displayName}!"
                        self.itemListOptions["currPage"] = 0
                        self.player.removeGold(price)
                        self.store.removeItem(item)
                        self.player.addItem(item)
                    else:
                        self.itemListOptions["message"] = f"{fore.RED}You can't afford the {item.displayName}!"
        elif action == "S":
            if self.itemListOptions["mode"] == "buy":
                self.itemListOptions["mode"] = "sell"
            else:
                item = self.selectItem(self.player, "Which item do you wish to sell?")
                if item:
                    self.player.incrementHistory("sell_item")
                    price = self.getItemPrice(item, "sell")
                    self.itemListOptions["message"] = f"{fore.YELLOW}You sold your {item.displayName}!"
                    self.itemListOptions["currPage"] = 0
                    self.player.addGold(price)
                    self.player.removeItem(item)
                    self.store.addItem(item)
        elif action == "P":
            self.itemListOptions["currPage"] -= 1
        elif action == "N":
            self.itemListOptions["currPage"] += 1
        elif action == "F":
            self.filterItems()
        elif action == "L":
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
        if not self.playerQuit:
            clear()
            self.printStats()
            self.printResolution()
            self.takeInput()

    def startNewGame(self):
        print("Choose a name:")
        name = input()
        self.player = Player(name)
        self.map = Map()

    def endGame(self):
        self.playerQuit = True

    def checkSavePath(self):
        if not os.path.exists(self.saveFilePath):
            os.makedirs(self.saveFilePath)

    def saveWorker(self, saveObj):
        saveFile = open(os.path.join(self.saveFilePath, self.saveId), 'w')
        json.dump(saveObj, saveFile)

    def createSave(self):
        self.checkSavePath()

        if self.saveId:
            saveId = self.saveId 
        else:
            saveId = str(int(time.time()))
            self.saveId = saveId

        sys.stdout.write(f"{style.DIM}.")
        saveObj = {
            "player": dict(copy.deepcopy(self.player).__dict__),
            "map": dict(copy.deepcopy(self.map).__dict__),
            "game": {
                "turn": self.turn,
                "nextLevel": self.nextLevel,
                "level": self.level,
                "ironman": self.ironman,
                "saveId": self.saveId
            }
        }

        # make player items serializable
        sys.stdout.write(fore.BLUE)
        saveObj["items"] = []
        for item in saveObj["player"]["items"]:
            sys.stdout.write(".")
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

        sys.stdout.write(fore.GREEN)
        for f, floor in enumerate(saveObj["map"]["floors"]):
            sys.stdout.write(".")
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

        sys.stdout.write(f"\n{style.RESET}")
        del saveObj["map"]["floors"]

        self.saveWorker(saveObj)

        try:
            with open(self.saveListFilePath) as json_file:  
                saveList = json.load(json_file)
        except:
            saveList = {}

        saveList[saveId] = f"{self.player.name} ({self.player.level})"
        if self.ironman:
            saveList[saveId] += f" {fore.STEEL_BLUE_3}[IRONMAN]{style.RESET}"

        with open(self.saveListFilePath, 'w') as outfile:  
            json.dump(saveList, outfile)