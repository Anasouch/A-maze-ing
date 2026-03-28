from typing import Dict, Tuple, List, Optional
import random


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
        if width < 3 or height < 3:
            raise ValueError("width and height must be at least 3")
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
        seed: Optional[int] = None,
    ) -> None:
        if width < 3 or height < 3:
            raise ValueError("width and height must be at least 3")
        self.width = width
        self.height = height
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
                self.crave_wall(x, y, direction)
                stack.append((nx, ny))
                found_unvisited = True
                break
            if found_unvisited is False:
                stack.pop()
        return self.grid

    def crave_wall(self, x: int, y: int, direction: str) -> None:
        self.grid.cells[y][x].open_wall(direction)
        opposite = Direction.get_opposite(direction)
        nx, ny = Direction.get_next_position(x, y, direction)
        self.grid.cells[ny][nx].open_wall(opposite)
