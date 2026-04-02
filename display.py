from mazegen import Grid, MazeGenerator
from typing import Tuple


class MazeDisplay:
    def __init__(self, maze: Grid):
        self.maze = maze

        # colors
        self.green = '\033[32m'
        self.red = '\033[31m'
        self.yellow = '\033[93m'
        self.blue = '\033[94m'
        self.orange = '\033[38;5;208m'
        self.reset = '\033[0m'

        # Emojies
        self.wall = "██"
        self.passage = "  "
        self.exit = "🚩"
        self.entry = f"{self.red}⚽︎{self.reset}"

    def set_color(self, choosen_color: int) -> None:
        if choosen_color == 1:
            self.wall = f"{self.green}██{self.reset}"
        elif choosen_color == 2:
            self.wall = f"{self.orange}██{self.reset}"
        elif choosen_color == 3:
            self.wall = f"{self.yellow}██{self.reset}"
        elif choosen_color == 4:
            self.wall = f"{self.blue}██{self.reset}"

    def display(
        self,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        choosen_color: int
    ) -> None:
        if choosen_color:
            self.set_color(choosen_color)

        WIDTH = self.maze.width
        HEIGHT = self.maze.height
        PASSAGE = self.passage
        ENTRY = self.entry
        EXIT = self.exit
        WALL = self.wall
        NUMBER_42 = f"{self.red}██{self.reset}"

        maze = []
        for _ in range(HEIGHT * 2 + 1):
            row = []
            for _ in range(WIDTH * 2 + 1):
                row.append(WALL)
            maze.append(row)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                cell = self.maze.get_cell(x, y)

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

                middle_x = self.maze.width // 2
                middle_y = self.maze.height // 2
                coordes = MazeGenerator.nbr_42coordes(
                    middle_x, middle_y, self.maze.width, self.maze.height
                    )
                if (x, y) in coordes:
                    maze[cy][cx] = NUMBER_42

        x, y = entry
        maze[y * 2 + 1][x * 2 + 1] = ENTRY

        x, y = exit
        maze[y * 2 + 1][x * 2 + 1] = EXIT

        for row in maze:
            line = ""
            for c in row:
                line += c
            print(line)
