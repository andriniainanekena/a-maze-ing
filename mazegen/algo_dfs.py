from mazegen.grid import Grid
from mazegen.maze_generator import MazeGenerator
from collections import deque
import random
import sys


class DepthFirstSearch(MazeGenerator):
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int,
    ) -> None:
        super().__init__(width, height, entry, exit, perfect, seed)
        random.seed(seed)

