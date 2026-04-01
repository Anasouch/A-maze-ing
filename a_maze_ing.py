from mazegen import MazeGenerator, Grid
from parsing import pars
from typing import Tuple
import random
import sys
import os


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


class MazeDisplay:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.b_green = '\033[92m'
        self.d_green = '\033[32m'
        self.red = '\033[31m'
        self.reset = '\033[0m'

        self.wall = "██"
        self.passage = "  "
        self.exit = f"{self.b_green}🌀{self.reset}"
        self.entry = f"{self.red}🐣{self.reset}"

    def set_color(self, choosen_color) -> None:
        if choosen_color == 1:
            self.wall = f"{self.d_green}██{self.reset}"
        elif choosen_color == 2:
            self.wall = f"{self.red}██{self.reset}"

    def display(
        self,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        choosen_color: int
    ) -> None:
        if choosen_color:
            self.set_color(choosen_color)
        width = self.grid.get_width()
        height = self.grid.get_height()
        PASSAGE = self.passage
        ENTRY = self.entry
        EXIT = self.exit
        WALL = self.wall

        maze = []
        for i in range(height * 2 + 1):
            row = []
            for j in range(width * 2 + 1):
                row.append(WALL)
            maze.append(row)

        for y in range(height):
            for x in range(width):
                cell = self.grid.get_cell(x, y)

                cx = x * 2 + 1
                cy = y * 2 + 1

                maze[cy][cx] = PASSAGE

                if not cell.has_wall("north"):
                    maze[cy - 1][cx] = PASSAGE
                if not cell.has_wall("south"):
                    maze[cy + 1][cx] = PASSAGE
                if not cell.has_wall("west"):
                    maze[cy][cx - 1] = PASSAGE
                if not cell.has_wall("east"):
                    maze[cy][cx + 1] = PASSAGE

        x, y = entry
        maze[y * 2 + 1][x * 2 + 1] = ENTRY

        x, y = exit
        maze[y * 2 + 1][x * 2 + 1] = EXIT

        for row in maze:
            line = ""
            for _ in row:
                line += _
            print(line)


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
    while True:
        maze = maze_gen.generate()

        display = MazeDisplay(maze)
        display.display(entry, exit, choosen_color=maze_color)
        print("\n=== A_maze_ing ===")
        print("1. Re_generate a new maze")
        print("2. Rotate maze colors")
        print("3. Quite\n")
        while True:
            try:
                choice = int(input("Enter a number from 1 to 3: "))
                if choice in range(1, 4):
                    break
                raise Exception()
            except Exception:
                print("\nTry again -> ", end="")
        if choice == 3:
            break
        elif choice == 2:
            if maze_color == 2:
                maze_color = 0
            else:
                maze_color += 1
        else:
            maze_gen.seed = random.randint(-2147483648, 2147483647)
        clear_terminal()
