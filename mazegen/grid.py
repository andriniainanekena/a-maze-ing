class Grid:
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000

    OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
    DELTA = {NORTH: (0, -1), SOUTH: (0, 1), EAST: (1, 0), WEST: (-1, 0)}

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: list[list[int]] = []
        self.create_grid()

    def create_grid(self) -> None:
        self.cells = []
        for y in range(self.height):
            line: list[int] = []
            for x in range(self.width):
                line.append(0xF)
            self.cells.append(line)

    def remove_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy = self.DELTA[direction]
        nx = x + dx
        ny = y + dy

        if not self.is_valid(nx, ny):
            return

        self.cells[y][x] &= ~direction
        self.cells[ny][nx] &= ~self.OPPOSITE[direction]

    def add_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy = self.DELTA[direction]
        nx = x + dx
        ny = y + dy

        if not self.is_valid(nx, ny):
            return

        self.cells[y][x] |= direction
        self.cells[ny][nx] |= self.OPPOSITE[direction]

    def is_valid(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
