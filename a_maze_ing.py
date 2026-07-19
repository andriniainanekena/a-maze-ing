import sys
from parsing.parsing_file import parse_input_file
from maze_display.ascii_renderer import ASCIIRenderer
from maze_build import generate_maze


def a_maze_ing(file_name: str) -> int:
    from input_choice import input_choices

    try:
        maze_setting = parse_input_file(file_name)
    except ValueError as e:
        print(e, file=sys.stderr)
        return -1

    if maze_setting.display_mode == "MLX":
        from maze_display.mlx_renderer import run_mlx

        return run_mlx(file_name, maze_setting)

    try:
        maze, solution = generate_maze(maze_setting)
    except Exception as e:
        print(e, file=sys.stderr)
        return -1

    if not solution:
        print("Couldn't find the maze's solution.", file=sys.stderr)
        return -1

    renderer = ASCIIRenderer(display_solution=maze_setting.display_solution)
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
