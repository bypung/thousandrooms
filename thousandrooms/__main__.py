import sys
import os

from .game import Game

clear=lambda: os.system('cls' if os.name == 'nt' else 'clear')

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    game = Game()
    while not game.quit:
        game.nextTurn()
    clear()


if __name__ == "__main__":
    main()