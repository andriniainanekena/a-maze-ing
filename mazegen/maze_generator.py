from mazegen.grid import Grid
from abc import ABC, abstractmethod
from typing import Any
import sys


class MazeGenerator(ABC):
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int] | None,
        perfect: bool,
        seed: int,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = Grid(width, height)
        self.logo = self.get_logo()

    @abstractmethod
    def generate(self) -> Any: ...

    @abstractmethod
    def solver(self) -> Any: ...

    def verif_3x3(self, nx: int, ny: int) -> bool:
        for ty in range(-2, 1):
            for tx in range(-2, 1):
                x = nx + tx
                y = ny + ty
                if (
                    self.grid.is_valid(x, y)
                    and self.grid.is_valid(x + 2, y + 2)
                ):
                    if self.is_there_hole(x, y):
                        return True
        return False

    def is_there_hole(self, nx: int, ny: int) -> bool:
        for y in range(3):
            for x in range(2):
                if self.grid.cells[ny + y][nx + x] & self.grid.EAST:
                    return False

        for y in range(2):
            for x in range(3):
                if self.grid.cells[ny + y][nx + x] & self.grid.SOUTH:
                    return False
        return True

    def create_hexa_maze(self) -> list[str]:
        hexa_maze: list[str] = []
        hexa = "0123456789ABCDEF"

        for lines in self.grid.cells:
            new_line: list[str] = []
            for cells in lines:
                new_cell = hexa[cells]
                new_line.append(new_cell)
            hexa_maze.append("".join(new_line))

        return hexa_maze

    def print_maze_to_file(
        self,
        file_name: str,
        hexa_maze: list[str],
        entry_to_exit_path: str,
    ) -> None:
        if self.exit is None:
            raise ValueError("Can't print the maze : there is no exit")

        x, y = self.entry
        x2, y2 = self.exit

        try:
            with open(file_name, "w") as file:
                file.write("\n".join(hexa_maze))
                file.write("\n\n")
                file.write(f"{x},{y}\n")
                file.write(f"{x2},{y2}\n")
                file.write(entry_to_exit_path + "\n")
        except OSError as e:
            print(e, file=sys.stderr)
            sys.exit(-1)

    def find_cardinal_path(
        self, path: list[tuple[int, int]] | None
    ) -> str:
        if path is None:
            raise ValueError(
                "Can't create a cardinal path : there is no path solution"
            )

        cardinal_path: list[str] = []
        for cell, next_cell in zip(path, path[1:]):
            x, y = cell
            x2, y2 = next_cell
            if x > x2:
                cardinal_path.append("W")
            if x2 > x:
                cardinal_path.append("E")
            if y > y2:
                cardinal_path.append("N")
            if y2 > y:
                cardinal_path.append("S")

        return "".join(cardinal_path)

    def get_logo(self) -> list[tuple[int, int]]:
        width = self.width
        while width > 9:
            height = self.height
            while height > 7:
                possible_logo = self.create_logo(width, height)
                if self.is_logo_valid(possible_logo):
                    return possible_logo
                height -= 1
            width -= 1
        return []

    def is_logo_valid(self, logo: list[tuple[int, int]]) -> bool:
        return self.entry not in logo and self.exit not in logo

    @staticmethod
    def create_logo(width: int, height: int) -> list[tuple[int, int]]:
        x = (width - 1) // 2
        y = (height - 1) // 2

        logo: list[tuple[int, int]] = [
            (x - 3, y - 2),
            (x - 3, y - 1),
            (x - 3, y),
            (x - 2, y),
            (x - 1, y),
            (x - 1, y + 1),
            (x - 1, y + 2),
            (x + 1, y - 2),
            (x + 2, y - 2),
            (x + 3, y - 2),
            (x + 3, y - 1),
            (x + 3, y),
            (x + 2, y),
            (x + 1, y),
            (x + 1, y + 1),
            (x + 1, y + 2),
            (x + 2, y + 2),
            (x + 3, y + 2),
        ]
        return logo
