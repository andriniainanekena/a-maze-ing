from mazegen.maze_generator import MazeGenerator
from mazegen.grid import Grid


RESET = ""


class ASCIIRenderer:
    def __init__(self, display_solution: bool) -> None:
        self.display_solution = display_solution

    def display_maze(
        self,
        maze: MazeGenerator,
        solution: list[tuple[int, int]],
    ) -> None:
        solution_set: set[tuple[int, int]] = set(solution)

        for y in range(maze.height):
            self._print_top_border(maze, y)
            self._print_cell_row(maze, y, solution_set)

        self._print_bottom_border(maze)

    def _print_top_border(self, maze: MazeGenerator, y: int) -> None:
        row = "+"
        for x in range(maze.width):
            has_north = bool(maze.grid.cells[y][x] & Grid.NORTH)
            row += "---+" if has_north else "   +"
        print(row)

    def _print_cell_row(
        self,
        maze: MazeGenerator,
        y: int,
        solution_set: set[tuple[int, int]],
    ) -> None:
        row = "|"

        for x in range(maze.width):
            char = self._get_cell_char(maze, x, y, solution_set)
            has_east = bool(maze.grid.cells[y][x] & Grid.EAST)

            row += f" {char} "
            row += "|" if has_east else " "

        print(row)

    def _get_cell_char(
        self,
        maze: MazeGenerator,
        x: int,
        y: int,
        solution_set: set[tuple[int, int]],
    ) -> str:
        if (x, y) == maze.entry:
            return "E"
        if (x, y) == maze.exit:
            return "X"
        if (x, y) in solution_set:
            return "o"
        return " "

    def _print_bottom_border(self, maze: MazeGenerator) -> None:
        row = "+"
        last_y = maze.height - 1

        for x in range(maze.width):
            has_south = bool(maze.grid.cells[last_y][x] & Grid.SOUTH)
            row += "---+" if has_south else "   +"

        print(row)