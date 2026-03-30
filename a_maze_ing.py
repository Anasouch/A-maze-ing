from mazegen import MazeGenerator, Grid
from parsing import pars
import sys


def display_maze(maze: Grid) -> None:
    pass


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
    maze = maze_gen.generate()
    display_maze(maze)
