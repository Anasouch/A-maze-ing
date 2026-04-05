from mazegen import MazeGenerator
from display import MazeDisplay
from mazepath import MazePath
from mazegen import Grid
from typing import List, Tuple, Optional
from parsing import pars
from time import sleep
import sys
import os


def path_animation(
        maze: Grid,
        path: List[Tuple[int, int]],
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        maze_color: int
) -> None:
    print('\033[?25l', end="")

    try:
        path_slices = []
        for i in range(len(path)):
            print('\033[H', end="")

            path_slices = path[:i]
            display = MazeDisplay(maze, path_slices)
            display.display(entry, exit, maze_color)

            print()
            print("=== A_maze_ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Path animation")
            print("5. Quit")
            print()

            if i < len(path) - 1:
                print("--> Enter a number from 1 to 5:  ", end="", flush=True)

            sleep(0.07)

    except (Exception, KeyboardInterrupt) as e:
        print(f"ERROR: {e}")

    finally:
        print('\033[?25h', end="")


if __name__ == "__main__":
    # Parsing
    conf_dict = pars()
    if not conf_dict:
        sys.exit(1)

    maze_gen = MazeGenerator(
        conf_dict["WIDTH"],
        conf_dict["HEIGHT"],
        conf_dict["ENTRY"],
        conf_dict["EXIT"],
        conf_dict["PERFECT"],
        conf_dict["SEED"]
        )
    maze = maze_gen.generate()

    entry = maze_gen.entry
    exit = maze_gen.exit
    seed = maze_gen.seed

    path_gen = MazePath(maze)
    path: Optional[List[Tuple[int, int]]] = path_gen.path(entry, exit)

    path = None
    maze_color = 0
    anim_displayed = 0
    while True:
        os.system('clear')

        if not path:
            displayed = 0
        else:
            displayed = 1

        display = MazeDisplay(maze, path)
        display.display(entry, exit, maze_color)

        print()
        print("=== A_maze_ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Path animation")
        print("5. Quit")
        print()

        while True:
            print('\033[?25l', end="")

            try:
                choice = int(input("--> Enter a number from 1 to 5: "))
                if choice in range(1, 6):
                    break
                raise Exception()

            except (Exception, KeyboardInterrupt):
                os.system('clear')

                display.display(entry, exit, maze_color)

                print()
                print("=== A_maze_ing ===")
                print("1. Re-generate a new maze")
                print("2. Show/Hide path from entry to exit")
                print("3. Rotate maze colors")
                print("4. Path animation")
                print("5. Quit")
                print()

                print("🔴 [FAILED] Try again")

            finally:
                print('\033[?25h', end="")

        if choice == 1:  # Re-generate a new maze
            if not maze_gen.seed:
                maze = maze_gen.generate()
                path = None
        elif choice == 2:  # Show/Hide path from entry to exit
            path_gen = MazePath(maze)
            path = path_gen.path(entry, exit)
            if displayed == 1:
                path = None
        elif choice == 3:  # Rotate maze colors
            if maze_color == 4:
                maze_color = 0
            else:
                maze_color += 1
        elif choice == 4:  # Path animation
            path_gen = MazePath(maze)
            path = path_gen.path(entry, exit)
            path_animation(maze, path, entry, exit, maze_color)
            anim_displayed = 1
        else:  # Quit
            os.system('clear')
            sys.exit(0)
