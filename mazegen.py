from typing import Dict, Tuple, List, Any
import random
import sys


def class_pars(conf_list: List[Any]) -> int:
    width = conf_list[0]
    height = conf_list[1]
    entry = conf_list[2]
    exit = conf_list[3]
    perfect = conf_list[4]
    seed = conf_list[5]

    try:
        width = int(width)
        height = int(height)

        if isinstance(entry, tuple) is False:
            raise ValueError(
                f"Invalid config {entry}, Entry and Exit must be tuples"
                )
        en1 = int(entry[0])
        en2 = int(entry[1])

        if isinstance(exit, tuple) is False:
            raise ValueError(
                f"Invalid config {exit}, Entry and Exit must be tuples"
                )
        ex1 = int(exit[0])
        ex2 = int(exit[1])

        if len(entry) != 2 or len(exit) != 2:
            raise ValueError(
                "Invalid config, Entry and Exit must include 2 cordinates"
                )

        if isinstance(perfect, bool) is False:
            raise ValueError(
                f"Invalid config '{perfect}', is not a value"
                )

        seed = int(seed)

        if width <= 0 or height <= 0:
            raise ValueError(
                "Invalid config, width and height must be greater than '0'"
                )

        if (
            ((en1 < 0) or (en2 < 0))
            or ((ex1 < 0) or (ex2 < 0))
        ):
            raise ValueError(
                "Invalid config, cordinates must be positive"
                )

        if (
            ((en1 >= width) or (en2 >= height))
            or ((ex1 >= width) or (ex2 >= height))
        ):
            raise ValueError(
                "Invalid config, cordinate is out of range"
                )

        if entry == exit:
            raise ValueError(
                "Invalid config, Entry and Exit must be different"
                )
    except Exception as e:
        print(f"Error: {e}")
        return 0
    return 1


class Cell:
    def __init__(self) -> None:
        self.walls: Dict[str, bool] = {
            "north": True,
            "west": True,
            "south": True,
            "east": True
        }

    def open_wall(self, direction: str) -> None:
        self.walls[direction] = False

    def has_wall(self, direction: str) -> bool:
        return self.walls[direction]

    def get_all_walls(self) -> Dict[str, bool]:
        return self.walls


class Direction:
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"

    MOVEMENTS: Dict[str, Tuple[int, int]] = {
        NORTH: (0, -1),
        EAST: (1, 0),
        SOUTH: (0, 1),
        WEST: (-1, 0),
    }

    OPPOSITES: Dict[str, str] = {
        NORTH: SOUTH,
        EAST: WEST,
        SOUTH: NORTH,
        WEST: EAST,
    }

    @staticmethod
    def get_next_position(
        x: int,
        y: int,
        direction: str,
    ) -> Tuple[int, int]:
        nx, ny = Direction.MOVEMENTS[direction]
        return (x + nx, y + ny)

    @staticmethod
    def get_opposite(direction: str) -> str:
        return Direction.OPPOSITES[direction]

    @staticmethod
    def get_all_directions() -> List[str]:
        return [
            Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST
            ]


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: List[List[Cell]] = []
        for _ in range(height):
            row: List[Cell] = []
            for _ in range(width):
                row.append(Cell())
            self.cells.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_width(self) -> int:
        return self.width

    def get_height(self) -> int:
        return self.height


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool,
        seed: int
    ) -> None:
        if not seed:
            seed = random.randint(-2147483648, 2147483647)
        conf_list = [width, height, entry, exit, perfect, seed]
        if class_pars(conf_list) == 0:
            sys.exit()
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate(self) -> Grid:
        self.grid = Grid(self.width, self.height)
        self.visited: List[List[bool]] = []
        for _ in range(self.height):
            row: List[bool] = []
            for _ in range(self.width):
                row.append(False)
            self.visited.append(row)

        random.seed(self.seed)
        self.visited[0][0] = True

        stack: List[Tuple[int, int]] = [(0, 0)]

        while stack:
            x, y = stack[-1]
            directions: List[str] = Direction.get_all_directions()
            random.shuffle(directions)

            found_unvisited = False
            for direction in directions:
                nx, ny = Direction.get_next_position(x, y, direction)

                if self.grid.is_in_bounds(nx, ny) is False:
                    continue
                if self.visited[ny][nx]:
                    continue

                self.visited[ny][nx] = True
                self.destroy_wall(x, y, direction)
                stack.append((nx, ny))
                found_unvisited = True
                break
            if found_unvisited is False:
                stack.pop()
        return self.grid

    def destroy_wall(self, x: int, y: int, direction: str) -> None:
        self.grid.cells[y][x].open_wall(direction)
        opposite = Direction.get_opposite(direction)
        nx, ny = Direction.get_next_position(x, y, direction)
        self.grid.cells[ny][nx].open_wall(opposite)
