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

