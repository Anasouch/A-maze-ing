from collections import deque
from mazegen import Grid, Direction
from typing import Tuple, List, Dict, Optional


class MazePath:
    def __init__(self, maze: Grid):
        self.maze = maze

    def path(
            self,
            entry: Tuple[int, int],
            exit: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        queue = deque([entry])
        visited = [entry]
        came_from: Dict[
            Tuple[int, int],
            Optional[Tuple[int, int]]
        ] = {entry: None}

        directions = Direction.get_all_directions()

        while True:
            x, y = queue.popleft()

            if (x, y) == exit:
                break

            cell = self.maze.get_cell(x, y)
            for direction in directions:
                nx, ny = Direction.get_next_position(x, y, direction)
                if (
                    (not cell.has_wall(direction))
                    and ((nx, ny) not in visited)
                ):
                    visited.append((nx, ny))
                    came_from[(nx, ny)] = (x, y)
                    queue.append((nx, ny))

        final_path = []
        current: Optional[Tuple[int, int]] = exit
        while current:
            final_path.append(current)
            current = came_from[current]
        final_path.reverse()
        return final_path
