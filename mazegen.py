from typing import Dict, Tuple, List, Any
import random
import sys


class InvalidConf(Exception):
    pass


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
        if width < 9 or height < 7:
            raise InvalidConf(
                "Invalid config, min dimensions is [WIDTH=9, HEIGHT=7]"
                )

        if isinstance(entry, tuple) is False:
            raise InvalidConf(
                f"Invalid config {entry}, Entry and Exit must be tuples"
                )
        en1 = int(entry[0])
        en2 = int(entry[1])

        if isinstance(exit, tuple) is False:
            raise InvalidConf(
                f"Invalid config {exit}, Entry and Exit must be tuples"
                )
        ex1 = int(exit[0])
        ex2 = int(exit[1])

        if len(entry) != 2 or len(exit) != 2:
            raise InvalidConf(
                "Invalid config, Entry and Exit must include 2 coordinates"
                )

        if isinstance(perfect, bool) is False:
            raise InvalidConf(
                f"Invalid config '{perfect}', is not a value"
                )

        if seed:
            seed = int(seed)

        if width <= 0 or height <= 0:
            raise InvalidConf(
                "Invalid config, width and height must be greater than '0'"
                )

        if (
            ((en1 < 0) or (en2 < 0))
            or ((ex1 < 0) or (ex2 < 0))
        ):
            raise InvalidConf(
                "Invalid config, coordinates must be positive"
                )

        if (
            ((en1 >= width) or (en2 >= height))
            or ((ex1 >= width) or (ex2 >= height))
        ):
            raise InvalidConf(
                "Invalid config, a coordinate is out of range"
                )

        if entry == exit:
            raise InvalidConf(
                "Invalid config, Entry and Exit must be different"
                )

        middle_x = width // 2
        middle_y = height // 2
        coordes = MazeGenerator.nbr_42coordes(
            middle_x, middle_y, width, height
            )
        if (entry in coordes) or (exit in coordes):
            raise InvalidConf(
                "Invalid config, Entry and Exit must out of [42] range"
                )
    except Exception as e:
        print(f"ERROR: {e}")
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
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST
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

    def is_in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
        perfect: bool,
        seed: int | None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

        # Parsing before generate
        conf_list = [width, height, entry, exit, perfect, seed]
        if class_pars(conf_list) == 0:
            sys.exit(1)

        # Fixed the Seed
        random.seed(self.seed)

    def generate(self) -> Grid:
        self.grid = Grid(self.width, self.height)
        self.visited: List[List[bool]] = []

        # Paint all cells
        for _ in range(self.height):
            row: List[bool] = []
            for _ in range(self.width):
                row.append(False)
            self.visited.append(row)

        self.visited[0][0] = True

        # Change the cells status of [42] to be visited
        middle_x = self.width // 2
        middle_y = self.height // 2
        self.coordes = self.nbr_42coordes(
            middle_x, middle_y, self.width, self.height
            )
        for x, y in self.coordes:
            self.visited[y][x] = True

        # [DFS] Algorithm
        stack: List[Tuple[int, int]] = [(0, 0)]
        while stack:
            x, y = stack[-1]
            directions: List[str] = Direction.get_all_directions()
            random.shuffle(directions)

            find_unvisited = False
            for direction in directions:
                nx, ny = Direction.get_next_position(x, y, direction)

                if self.grid.is_in_bounds(nx, ny) is False:
                    continue
                if self.visited[ny][nx]:
                    continue

                self.destroy_wall(x, y, direction)
                stack.append((nx, ny))
                find_unvisited = True
                self.visited[ny][nx] = True
                break
            if find_unvisited is False:
                stack.pop()
        return self.grid

    def destroy_wall(self, x: int, y: int, direction: str) -> None:
        self.grid.cells[y][x].open_wall(direction)
        opposite = Direction.get_opposite(direction)
        nx, ny = Direction.get_next_position(x, y, direction)
        self.grid.cells[ny][nx].open_wall(opposite)

    # Get [42] coordinates
    @staticmethod
    def nbr_42coordes(
        x: int, y: int, width: int, height: int
    ) -> List[Tuple[int, int]]:
        coordes = []

        # Common "4" part
        coordes.append((x - 1, y))
        coordes.append((x - 2, y))
        coordes.append((x - 3, y))
        coordes.append((x - 1, y + 1))
        coordes.append((x - 1, y + 2))
        coordes.append((x - 1, y - 1))

        # Common "2" part
        coordes.append((x + 1, y))
        coordes.append((x + 2, y))
        coordes.append((x + 3, y))
        coordes.append((x + 1, y + 1))
        coordes.append((x + 1, y + 2))
        coordes.append((x + 2, y + 2))
        coordes.append((x + 3, y + 2))
        coordes.append((x + 3, y - 1))
        coordes.append((x + 3, y - 2))

        # Even Width
        if width % 2 == 0:
            # Number "4"
            coordes.append((x - 4, y))
            coordes.append((x - 4, y - 1))
            coordes.append((x - 4, y - 2))

        # Odd Width
        else:
            # Number "4"
            coordes.append((x - 3, y - 1))
            coordes.append((x - 3, y - 2))

        # Even Height
        if height % 2 == 0:

            # Number "4"
            if width % 2 == 0:
                coordes.append((x - 4, y - 3))
            else:
                coordes.append((x - 3, y - 3))

            # Number "2"
            coordes.append((x + 1, y - 3))
            coordes.append((x + 2, y - 3))
            coordes.append((x + 3, y - 3))
            coordes.append((x - 1, y - 2))

        # Odd Height
        else:
            # Number "2"
            coordes.append((x + 1, y - 2))
            coordes.append((x + 2, y - 2))

        return coordes


class MazeOutput:

    @staticmethod
    def cell_to_hex(cell: Cell) -> int:
        value = 0

        if cell.has_wall("north"):
            value += 1
        if cell.has_wall("east"):
            value += 2
        if cell.has_wall("south"):
            value += 4
        if cell.has_wall("west"):
            value += 8

        return value

    def save(
        self,
        grid: Grid,
        filename: str,
        entry: Tuple[int, int],
        exit_pos: Tuple[int, int]
    ) -> None:

        with open(filename, "w") as f:
            for y in range(grid.height):
                line = ""
                for x in range(grid.width):
                    cell = grid.get_cell(x, y)
                    hex_value = self.cell_to_hex(cell)
                    line += format(hex_value, "X")
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
