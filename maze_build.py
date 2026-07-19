from mazegen.algo_dfs import DepthFirstSearch
from mazegen.maze_generator import MazeGenerator
from parsing.valid_file_input import ValidFileInput


def generate_maze(
    maze_setting: ValidFileInput,
) -> tuple[MazeGenerator, list[tuple[int, int]] | None]:
    maze = DepthFirstSearch(
        width=maze_setting.width,
        height=maze_setting.height,
        entry=(maze_setting.entry_x, maze_setting.entry_y),
        exit=(maze_setting.exit_x, maze_setting.exit_y),
        perfect=maze_setting.is_perfect,
        seed=maze_setting.seed,
    )

    maze.generate()
    hexa_maze = maze.create_hexa_maze()

    perfect_maze_path = maze.solver()
    cardinal_path = maze.find_cardinal_path(perfect_maze_path)
    maze.print_maze_to_file(
        maze_setting.output_filename, hexa_maze, cardinal_path
    )

    solution = maze.solver()
    return maze, solution
