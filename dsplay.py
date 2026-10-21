from mazegen import MazeGenerator
from mazegen.generator import DIRECTIONS
from output_writer import write_output

RESET = "\033[0m"
CLEAR_SCREEN = "\033[2J\033[H"
COLORS = {
    "white": "\033[97m",
    "cyan": "\033[96m",
    "magenta": "\033[95m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "green": "\033[92m",
    "red": "\033[91m",
}
COLOR_NAMES = ["white", "cyan", "magenta", "yellow", "blue"]
BLOCK = "██"

WALL = "#"
EMPTY = " "
PATTERN = "4"
PATH = "."
ENTRY = "E"
EXIT = "X"

def build_char_grid(gen: MazeGenerator, path_letters: str,
                    show_path: bool) -> list[list[str]]:
    """Turn the walls into a grid of squares ready to draw"""

    grid = []
    for row in range(2 * gen.heigth + 1):
        line = []
        for column in range(2 * gen.width + 1):
            line.append(WALL)
        grid.append(line)

    for y in range(gen.height):
        for x in range(gen.width):
            grid_x = 2 * x + 1
            grid_y = 2 * y + 1
            if (x, y) in gen.pattern_cells:
                grid[grid_y][grid_x] = PATTERN
            else:
                grid[grid_y][grid_x] = EMPTY
            if not gen.walls[y][x]["E"]:
                grid[grid_y][grid_x + 1] = EMPTY
            if not gen.walls[y][x]["S"]:
                grid[grid_y + 1][grid_x] = EMPTY

    if show_path:
        grid_x = 2 * gen.entry_pos[0] + 1
        grid_y = 2 * gen.entry_pos[1] + 1
        for letter in path_letters:
           move = DIRECTIONS[letter]
            for square in range(2):

