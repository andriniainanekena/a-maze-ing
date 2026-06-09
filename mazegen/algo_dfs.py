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


    def generate(self) -> None:
        stack = [self.entry]
        visited = {self.entry}
        visited.update(self.logo)

        while stack:
            current_cell = stack[-1]
            neighbors = self.get_unvisited_neighbors(current_cell, visited)
            if neighbors:
                direction = random.choice(neighbors)
                x, y = current_cell
                self.grid.remove_wall(x, y, direction)
                dx, dy = self.grid.DELTA[direction]
                nx, ny = x + dx, y + dy
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()
        if not self.perfect:
            self.maze_imperfect()


    def get_unvisited_neighbors(
        self,
        cell: tuple[int, int],
        visited: set[tuple[int, int]],
    ) -> list[int]:
        g = self.grid
        x, y = cell
        neighbors = []

        for direction in [g.NORTH, g.SOUTH, g.EAST, g.WEST]:
            dx, dy = g.DELTA[direction]
            nx, ny = x + dx, y + dy
            if g.is_valid(nx, ny) and (nx, ny) not in visited:
                neighbors.append(direction)
        return neighbors
