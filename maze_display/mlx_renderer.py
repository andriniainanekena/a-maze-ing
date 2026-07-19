import sys
from typing import Callable
from mlx import Mlx
from mazegen.maze_generator import MazeGenerator
from mazegen.grid import Grid
from parsing.valid_file_input import ValidFileInput

CELL = 24
WALL_THICKNESS = 3
MARGIN = 20
INFO_HEIGHT = 50
ANIM_SPEED = 2
STEPS_PER_TICK = 2
LINE_WIDTH = CELL // 3

KEY_1 = 49
KEY_2 = 50
KEY_3 = 51
KEY_4 = 52
KEY_ESCAPE = 65307
EVENT_CLOSE = 33

OPAQUE = 0xFF000000

COLOR_SETS = [
    {
        "wall": OPAQUE | 0xF5F5F5,
        "floor": OPAQUE | 0x101010,
        "entry": OPAQUE | 0x00E676,
        "exit": OPAQUE | 0xFF1744,
        "logo": OPAQUE | 0x4D4D4D,
        "solution": OPAQUE | 0x2979FF,
        "background": OPAQUE | 0x000000,
    },
    {
        "wall": OPAQUE | 0xAB47BC,
        "floor": OPAQUE | 0x0D0D14,
        "entry": OPAQUE | 0xFFEE58,
        "exit": OPAQUE | 0xFF4081,
        "logo": OPAQUE | 0x37474F,
        "solution": OPAQUE | 0x00E5FF,
        "background": OPAQUE | 0x000000,
    },
    {
        "wall": OPAQUE | 0xFFA726,
        "floor": OPAQUE | 0x101010,
        "entry": OPAQUE | 0x29B6F6,
        "exit": OPAQUE | 0xEF5350,
        "logo": OPAQUE | 0x5D4037,
        "solution": OPAQUE | 0xD4E157,
        "background": OPAQUE | 0x000000,
    },
    {
        "wall": OPAQUE | 0x42A5F5,
        "floor": OPAQUE | 0x0D0D14,
        "entry": OPAQUE | 0xFF7043,
        "exit": OPAQUE | 0x66BB6A,
        "logo": OPAQUE | 0x8E24AA,
        "solution": OPAQUE | 0xFFEB3B,
        "background": OPAQUE | 0x000000,
    },
]


class MLXRenderer:
    def __init__(
        self,
        maze: MazeGenerator,
        solution: list[tuple[int, int]],
        display_solution: bool,
        color_index: int = 0,
    ) -> None:
        self.maze = maze
        self.solution = solution
        self.display_solution = display_solution
        self.color_index = color_index
        self.anim_progress = 0
        self.animating = display_solution
        self.frame_counter = 0
        self.logo_set: set[tuple[int, int]] = set(maze.logo)
        self.on_regenerate: Callable[[], None] | None = None

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        width_px = MARGIN * 2 + maze.width * CELL
        height_px = MARGIN * 2 + maze.height * CELL + INFO_HEIGHT
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, width_px, height_px, "A-Maze-ing"
        )

    @property
    def colors(self) -> dict[str, int]:
        return COLOR_SETS[self.color_index]

    def set_maze(
        self, maze: MazeGenerator, solution: list[tuple[int, int]]
    ) -> None:
        self.maze = maze
        self.solution = solution
        self.logo_set = set(maze.logo)
        self.anim_progress = 0
        self.frame_counter = 0
        self.animating = self.display_solution
        self.draw_static()

    def draw_static(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self._fill_cell(x, y, self._cell_color(x, y))
        self._draw_walls()
        self._draw_info()
        if self.display_solution:
            self._reveal_up_to(self.anim_progress)

    def start(self) -> None:
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._on_loop, None)
        self.mlx.mlx_key_hook(self.win_ptr, self._on_key, None)
        self.mlx.mlx_hook(self.win_ptr, EVENT_CLOSE, 0, self._on_close, None)
        self.mlx.mlx_loop(self.mlx_ptr)

    def _cell_color(self, x: int, y: int) -> int:
        if (x, y) in self.logo_set:
            return self.colors["logo"]
        if (x, y) == self.maze.entry:
            return self.colors["entry"]
        if (x, y) == self.maze.exit:
            return self.colors["exit"]
        return self.colors["floor"]

    def _fill_cell(self, x: int, y: int, color: int) -> None:
        px = MARGIN + x * CELL
        py = MARGIN + y * CELL
        for yy in range(py, py + CELL):
            for xx in range(px, px + CELL):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, xx, yy, color
                )

    def _put_solution_pixel(self, x: int, y: int, color: int) -> None:
        cell_x = (x - MARGIN) // CELL
        cell_y = (y - MARGIN) // CELL
        if (cell_x, cell_y) == self.maze.entry:
            return
        if (cell_x, cell_y) == self.maze.exit:
            return
        self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def _draw_solution_marker(self, x: int, y: int) -> None:
        inner = (CELL - LINE_WIDTH) // 2
        px = MARGIN + x * CELL + inner
        py = MARGIN + y * CELL + inner
        color = self.colors["solution"]
        for yy in range(py, py + LINE_WIDTH):
            for xx in range(px, px + LINE_WIDTH):
                self._put_solution_pixel(xx, yy, color)

    def _draw_solution_connector(
        self, a: tuple[int, int], b: tuple[int, int]
    ) -> None:
        ax, ay = a
        bx, by = b
        offset = (CELL - LINE_WIDTH) // 2
        color = self.colors["solution"]
        if ax == bx:
            px = MARGIN + ax * CELL + offset
            py = MARGIN + min(ay, by) * CELL + offset
            width, height = LINE_WIDTH, CELL
        else:
            px = MARGIN + min(ax, bx) * CELL + offset
            py = MARGIN + ay * CELL + offset
            width, height = CELL, LINE_WIDTH
        for yy in range(py, py + height):
            for xx in range(px, px + width):
                self._put_solution_pixel(xx, yy, color)

    def _reveal_up_to(self, count: int) -> None:
        count = max(0, min(count, len(self.solution)))
        if count == 0:
            return
        self._draw_solution_marker(*self.solution[0])
        for i in range(1, count):
            self._draw_solution_connector(
                self.solution[i - 1], self.solution[i]
            )
            self._draw_solution_marker(*self.solution[i])

    def _draw_wall_h(self, x0: int, y0: int, length: int) -> None:
        color = self.colors["wall"]
        for t in range(WALL_THICKNESS):
            for x in range(x0, x0 + length + WALL_THICKNESS):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, x, y0 + t, color
                )

    def _draw_wall_v(self, x0: int, y0: int, length: int) -> None:
        color = self.colors["wall"]
        for t in range(WALL_THICKNESS):
            for y in range(y0, y0 + length + WALL_THICKNESS):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win_ptr, x0 + t, y, color
                )

    def _draw_walls(self) -> None:
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.grid.cells[y][x]
                px = MARGIN + x * CELL
                py = MARGIN + y * CELL
                if cell & Grid.NORTH:
                    self._draw_wall_h(px, py, CELL)
                if cell & Grid.WEST:
                    self._draw_wall_v(px, py, CELL)
                if x == self.maze.width - 1 and cell & Grid.EAST:
                    self._draw_wall_v(px + CELL, py, CELL)
                if y == self.maze.height - 1 and cell & Grid.SOUTH:
                    self._draw_wall_h(px, py + CELL, CELL)

    def _draw_info(self) -> None:
        y = MARGIN * 2 + self.maze.height * CELL + 10
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            MARGIN,
            y,
            OPAQUE | 0xFFFFFF,
            "1:Regenerate  2:Path  3:Colors  4/Esc:Quit",
        )
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            MARGIN,
            y + 20,
            OPAQUE | 0xFFFFFF,
            f"Seed: {self.maze.seed}",
        )

    def _toggle_solution(self) -> None:
        if self.display_solution:
            self.display_solution = False
            self.animating = False
            self.anim_progress = 0
        else:
            self.display_solution = True
            self.animating = True
            self.anim_progress = 0
        self.draw_static()

    def _rotate_color(self) -> None:
        self.color_index = (self.color_index + 1) % len(COLOR_SETS)
        self.draw_static()

    def _on_loop(self, param: object) -> None:
        if not self.animating:
            return
        self.frame_counter += 1
        if self.frame_counter < ANIM_SPEED:
            return
        self.frame_counter = 0
        if self.anim_progress >= len(self.solution):
            self.animating = False
            return
        next_progress = min(
            self.anim_progress + STEPS_PER_TICK, len(self.solution)
        )
        for i in range(self.anim_progress, next_progress):
            if i == 0:
                self._draw_solution_marker(*self.solution[0])
            else:
                self._draw_solution_connector(
                    self.solution[i - 1], self.solution[i]
                )
                self._draw_solution_marker(*self.solution[i])
        self.anim_progress = next_progress

    def _on_key(self, keycode: int, param: object) -> None:
        if keycode == KEY_1 and self.on_regenerate is not None:
            self.on_regenerate()
        elif keycode == KEY_2:
            self._toggle_solution()
        elif keycode == KEY_3:
            self._rotate_color()
        elif keycode in (KEY_4, KEY_ESCAPE):
            self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _on_close(self, param: object) -> None:
        self.mlx.mlx_loop_exit(self.mlx_ptr)


def run_mlx(file_name: str, maze_setting: ValidFileInput) -> int:
    from maze_build import generate_maze

    try:
        maze, solution = generate_maze(maze_setting)
    except Exception as e:
        print(e, file=sys.stderr)
        return -1

    if not solution:
        print("Couldn't find the maze's solution.", file=sys.stderr)
        return -1

    renderer = MLXRenderer(maze, solution, maze_setting.display_solution)

    def regenerate() -> None:
        from parsing.parsing_file import parse_input_file

        try:
            new_setting = parse_input_file(file_name)
            new_maze, new_solution = generate_maze(new_setting)
        except Exception as e:
            print(e, file=sys.stderr)
            return
        if not new_solution:
            print("Couldn't find the maze's solution.", file=sys.stderr)
            return
        renderer.set_maze(new_maze, new_solution)

    renderer.on_regenerate = regenerate
    renderer.draw_static()
    renderer.start()
    return 0
