from mazegen.maze_generator import MazeGenerator
from mazegen.grid import Grid

RESET = "\033[0m"

COLOR_SETS = [
    {
        "wall": "\033[38;5;250m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;46m",
        "exit": "\033[38;5;196m",
        "logo": "\033[38;5;208m",
        "solution": "\033[38;5;51m",
    },
    {
        "wall": "\033[38;5;99m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;226m",
        "exit": "\033[38;5;201m",
        "logo": "\033[38;5;39m",
        "solution": "\033[38;5;82m",
    },
    {
        "wall": "\033[38;5;214m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;27m",
        "exit": "\033[38;5;160m",
        "logo": "\033[38;5;129m",
        "solution": "\033[38;5;190m",
    },
    {
        "wall": "\033[38;5;33m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;202m",
        "exit": "\033[38;5;118m",
        "logo": "\033[38;5;199m",
        "solution": "\033[38;5;229m",
    },
    {
        "wall": "\033[38;5;244m",
        "tunnel": "\033[0m",
        "entry": "\033[38;5;45m",
        "exit": "\033[38;5;220m",
        "logo": "\033[38;5;93m",
        "solution": "\033[38;5;154m",
    },
]


class ASCIIRenderer:
    def __init__(
        self, display_solution: bool, color_index: int = 0
    ) -> None:
        self.display_solution = display_solution
        self.color_index = color_index

    @property
    def colors(self) -> dict[str, str]:
        return COLOR_SETS[self.color_index]

    def next_color(self) -> None:
        self.color_index = (self.color_index + 1) % len(COLOR_SETS)

    def _c(self, key: str, text: str) -> str:
        return self.colors[key] + text + RESET

    def display_maze(
        self,
        maze: MazeGenerator,
        solution: list[tuple[int, int]],
    ) -> None:
        solution_set: set[tuple[int, int]] = set(solution)
        logo_set: set[tuple[int, int]] = set(maze.logo)

        for y in range(maze.height):
            self._print_top_border(maze, y)
            self._print_cell_row(maze, y, solution_set, logo_set)

        self._print_bottom_border(maze)

        print(f"\nSeed: {maze.seed}")
        if not maze.logo:
            print("Can't print 42 logo : the maze is too small")

    def _print_top_border(self, maze: MazeGenerator, y: int) -> None:
        row = self._c("wall", "+")
        for x in range(maze.width):
            has_north = bool(maze.grid.cells[y][x] & Grid.NORTH)
            seg = "---" if has_north else "   "
            row += self._c("wall", seg) + self._c("wall", "+")
        print(row)

    def _print_cell_row(
        self,
        maze: MazeGenerator,
        y: int,
        solution_set: set[tuple[int, int]],
        logo_set: set[tuple[int, int]],
    ) -> None:
        row = self._c("wall", "|")
        for x in range(maze.width):
            color_key, char = self._get_cell(
                maze, x, y, solution_set, logo_set
            )
            has_east = bool(maze.grid.cells[y][x] & Grid.EAST)
            row += self._c(color_key, f" {char} ")
            row += self._c("wall", "|") if has_east else "   "[1]
        print(row)

    def _get_cell(
        self,
        maze: MazeGenerator,
        x: int,
        y: int,
        solution_set: set[tuple[int, int]],
        logo_set: set[tuple[int, int]],
    ) -> tuple[str, str]:
        if (x, y) in logo_set:
            return "logo", "x"
        if (x, y) == maze.entry:
            return "entry", "E"
        if (x, y) == maze.exit:
            return "exit", "X"
        if self.display_solution and (x, y) in solution_set:
            return "solution", "o"
        return "tunnel", " "

    def _print_bottom_border(self, maze: MazeGenerator) -> None:
        row = self._c("wall", "+")
        for x in range(maze.width):
            last_y = maze.height - 1
            has_south = bool(maze.grid.cells[last_y][x] & Grid.SOUTH)
            seg = "---" if has_south else "   "
            row += self._c("wall", seg) + self._c("wall", "+")
        print(row)

    def print_menu(self) -> None:
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
