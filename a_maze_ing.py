from mazegen import MazeGenerator
from display import MazeDisplay
from parsing import pars
import random
import sys
import os


def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    conf_dict = pars()
    if not conf_dict:
        sys.exit()
    maze_gen = MazeGenerator(
        conf_dict["WIDTH"],
        conf_dict["HEIGHT"],
        conf_dict["ENTRY"],
        conf_dict["EXIT"],
        conf_dict["PERFECT"],
        conf_dict["SEED"]
        )
    entry = maze_gen.entry
    exit = maze_gen.exit
    seed = maze_gen.seed
    maze_color = 0
    choice = 1
    while True:
        if choice == 1:
            maze = maze_gen.generate()

        clear_terminal()
        display = MazeDisplay(maze)
        display.display(entry, exit, maze_color)

        print()
        print("=== A_maze_ing ===")
        print("1. Re-generate a new maze")
        print("2. Rotate maze colors")
        print("3. Quit")
        print()

        while True:
            try:
                choice = int(input("Enter a number from 1 to 3: "))
                if choice in range(1, 4):
                    break
                raise Exception()
            except Exception:
                print("\nTry again -> ", end="")
        if choice == 3:
            sys.exit()
        elif choice == 2:
            if maze_color == 4:
                maze_color = 0
            else:
                maze_color += 1
        else:
            seed = random.randint(-2147483648, 2147483647)
