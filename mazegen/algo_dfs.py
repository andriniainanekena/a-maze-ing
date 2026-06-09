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

    def maze_imperfect(self) -> None:
        lst: list[int] = [1, 2, 3]
        directions: list[int] = [
            Grid.NORTH, Grid.SOUTH, Grid.EAST, Grid.WEST
        ]
        for y in range(self.height):
            for x in range(self.width):
                res = random.choice(lst)
                if res == 3:
                    direction = random.choice(directions)
                    dx, dy = self.grid.DELTA[direction]
                    nx, ny = x + dx, y + dy
                    if (
                        self.grid.is_valid(nx, ny)
                        and (nx, ny) not in self.logo
                        and (x, y) not in self.logo
                    ):
                        self.grid.remove_wall(x, y, direction)
                        if self.verif_3x3(x, y):
                            self.grid.add_wall(x, y, direction)

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


if __name__ == "__main__":
    try:
        dfs = DepthFirstSearch(10, 10, (2, 4), (9, 9), perfect=True, seed=42)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit()

    dfs.generate()
    hexa_maze = dfs.create_hexa_maze()
    perfect_maze_path = dfs.solver()
    try:
        cardinal_path = dfs.find_cardinal_path(perfect_maze_path)
    except ValueError as e:
        print(e)
    else:
        dfs.print_maze_to_file("file.txt", hexa_maze, cardinal_path)
