import os
import sys
from mazegen.maze_generator import MazeGenerator
from maze_display.ascii_renderer import ASCIIRenderer


def input_choices(
    maze: MazeGenerator,
    renderer: ASCIIRenderer,
    solution: list[tuple[int, int]],
    file_name: str,
) -> None:
    from a_maze_ing import a_maze_ing

    renderer.print_menu()
    choice = input("Choice? (1-4): ")
    os.system("clear")

    if choice == "1":
        a_maze_ing(file_name)

    elif choice == "2":
        renderer.display_solution = not renderer.display_solution
        renderer.display_maze(maze, solution)
        input_choices(maze, renderer, solution, file_name)

    elif choice == "3":
        renderer.next_color()
        renderer.display_maze(maze, solution)
        input_choices(maze, renderer, solution, file_name)

    elif choice == "4":
        sys.exit(0)

    else:
        renderer.display_maze(maze, solution)
        input_choices(maze, renderer, solution, file_name)
