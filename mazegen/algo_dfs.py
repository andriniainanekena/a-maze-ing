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

    def solver(self) -> list[tuple[int, int]] | None:
        parent: dict[tuple[int, int], tuple[int, int] | None] = {
            self.entry: None
        }
        visited: set[tuple[int, int]] = {self.entry}
        queue: deque[tuple[int, int]] = deque([self.entry])

        while queue:
            current_cell: tuple[int, int] = queue.popleft()
            if current_cell == self.exit:
                return self.get_path_way(parent)
            x, y = current_cell
            for neighbor in self.get_neighbors(x, y):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_cell
                    queue.append(neighbor)
        return None

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        g = self.grid
        neighbors = []

        for direction in [g.NORTH, g.SOUTH, g.EAST, g.WEST]:
            if not (g.cells[y][x] & direction):
                dx, dy = g.DELTA[direction]
                nx, ny = x + dx, y + dy
                if g.is_valid(nx, ny):
                    neighbors.append((nx, ny))
        return neighbors

    def get_path_way(
        self,
        parent: dict[tuple[int, int], tuple[int, int] | None],
    ) -> list[tuple[int, int]]:
        path = []
        current: tuple[int, int] | None = self.exit

        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path

