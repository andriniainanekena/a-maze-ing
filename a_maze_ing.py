import sys
from parsing.parsing_file import parse_input_file
from mazegen.algo_dfs import DepthFirstSearch
from maze_display.ascii_renderer import ASCIIRenderer


def a_maze_ing(file_name: str) -> int:
    from input_choice import input_choices

    try:
        maze_setting = parse_input_file(file_name)
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1

    try:
        maze = DepthFirstSearch(
            width=maze_setting.width,
            height=maze_setting.height,
            entry=(maze_setting.entry_x, maze_setting.entry_y),
            exit=(maze_setting.exit_x, maze_setting.exit_y),
            perfect=maze_setting.is_perfect,
            seed=maze_setting.seed,
        )
        renderer = ASCIIRenderer(
            display_solution=maze_setting.display_solution,
        )
    except Exception as e:
        print(e, file=sys.stderr)
        return -1

    maze.generate()
    hexa_maze = maze.create_hexa_maze()

    perfect_maze_path = maze.solver()
    try:
        cardinal_path = maze.find_cardinal_path(perfect_maze_path)
        maze.print_maze_to_file(
            maze_setting.output_filename, hexa_maze, cardinal_path
        )
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1

    solution = maze.solver()
    if not solution:
        print("Couldn't find the maze's solution.", file=sys.stderr)
        return -1

    renderer.display_maze(maze, solution)

    try:
        input_choices(maze, renderer, solution, file_name)
    except (KeyboardInterrupt, EOFError):
        return 0
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("You can't have more than 1 argument.\n", file=sys.stderr)
        sys.exit(-1)

    if len(sys.argv) == 1:
        print("You can't have no argument.", file=sys.stderr)
        sys.exit(-1)

    a_maze_ing(sys.argv[1])
