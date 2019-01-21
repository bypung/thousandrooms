import sys
import os
import json
import dill as pickle

from colored import fore, back, style
import colorama

from .game import Game
from .player import Player
from .maps import Map

clear=lambda: os.system('cls' if os.name == 'nt' else 'clear')

class Launcher:
    saveFilePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), "save")
    saveListFilePath = os.path.join(saveFilePath, "saveList.json")
    game = None

    def checkSavePath(self):
        if not os.path.exists(self.saveFilePath):
            os.makedirs(self.saveFilePath)

    def loadSaveFiles(self):
        try:
            with open(self.saveListFilePath) as json_file:  
                saveList = json.load(json_file)
        except:
            saveList = {}
        
        out = []
        for (key, value) in saveList.items():
            out.append({
                "saveId": key,
                "name": value
            })

        return out

    def deleteSave(self, saveId):
        try:
            with open(self.saveListFilePath, "r") as json_file:
                saveList = json.load(json_file)
        except:
            return
        
        try:
            del saveList[saveId]
            with open(self.saveListFilePath, "w") as json_file:
                json.dump(saveList, json_file)
            os.remove(os.path.join(self.saveFilePath, saveId))
        except KeyError:
            pass

    def loadSave(self, load):
        loadFile = open(os.path.join(self.saveFilePath, load["saveId"]), "r")  
        load = json.load(loadFile)
        return load

    def printSaveList(self, saveList):
        for i, save in enumerate(saveList):
            print(f"{i + 1}) {save['name']}")

    def startNewGame(self):
        self.game = Game()
        print("Choose a name:")
        name = input()
        self.game.player = Player(name)
        self.game.map = Map()
        print(f"<I>ronman Mode? {style.DIM}<Enter> for no{style.RESET}")
        ironman = input()
        if len(ironman) > 0 and ironman[0].upper() == "I":
            self.game.ironman = True
        self.runGame()

    def runGame(self):
        while not self.game.playerQuit and not self.game.restart:
            self.game.nextTurn()

    def startGame(self):
        clear()
        gameStarted = False

        print(f"{style.BOLD}Welcome To The Dungeon of 1000 Rooms!\n")
        print(f"<L>oad, <N>ew{style.RESET}")
        
        while not gameStarted:
            action = input()
            if len(action) > 0:
                action = action[0].upper()
            if action == "L":            
                saves = self.loadSaveFiles()
                if saves and len(saves) > 0:
                    clear()
                    self.printSaveList(saves)
                    saveFile = None
                    while not saveFile:
                        sys.stdout.write(f"\n{style.BOLD}Choose a save file: ")
                        saveChoice = input()
                        try:
                            saveIndex = int(saveChoice) - 1
                            saveFile = saves[saveIndex]
                            load = self.loadSave(saveFile)
                            self.game = Game()
                            self.game.player = Player(load["player"]["name"], load["player"])
                            self.game.player.loadItems(load["items"])
                            for i in load["game"]:
                                setattr(self.game, i, load["game"][i])
                            self.game.map = Map(load["map"]["numFloors"], load["map"]["width"], load["map"])

                            if self.game.ironman:
                                self.deleteSave(self.game.saveId)
                                self.game.saveId = ""

                            gameStarted = True
                            self.runGame()
                        except IndexError:
                            print("Invalid item number")
                        except ValueError:
                            print("Please enter an integer")
                else:
                    print ("No save file found, let's start a new game instead!")
                    gameStarted = True
                    self.startNewGame()
            elif action == "N":
                gameStarted = True
                self.startNewGame()

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    launcher = Launcher()
    while not launcher.game or not launcher.game.playerQuit:
        launcher.startGame()
    if launcher.game.playerQuit:
        clear()
        launcher.game.player.printHistory(launcher.game.turn)
        print()

if __name__ == "__main__":
    colorama.init()
    main()
    colorama.deinit()