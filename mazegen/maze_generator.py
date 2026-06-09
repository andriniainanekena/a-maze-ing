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
