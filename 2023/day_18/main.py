from utils import files
from utils import maths
from collections import deque
from collections import Counter


# Day 18: Lavaduct Lagoon
# https://adventofcode.com/2023/day/28


DIRECTION_MAP = {
    'U': (0, -1),
    'D': (0, 1),
    'R': (1, 0),
    'L': (-1, 0),
}

HEX_DIRECTION_MAP = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
}


def get_dig_plan() -> list[tuple[str, int, str]]:
    lines = files.read_file('data.txt')
    dig_plan = []

    for line in lines:
        parts = line.split(' ')
        dig_plan.append((parts[0], int(parts[1]), parts[2]))

    return dig_plan


def instruction_fits_inside_grid(dig_grid: list[list[str]], new_x: int, new_y: int) -> bool:
    return 0 <= new_x < len(dig_grid[0]) and 0 <= new_y < len(dig_grid)


def extend_grid(dig_grid: list[list[str]], direction: str, new_x: int, new_y: int) -> list[list[str]]:
    if direction == 'U':
        new_rows_needed = abs(new_y)
        for _ in range(new_rows_needed):
            dig_grid.insert(0, ['.'] * len(dig_grid[0]))

    elif direction == 'D':
        new_rows_needed = new_y - len(dig_grid) + 1
        for _ in range(new_rows_needed):
            dig_grid.append(['.'] * len(dig_grid[0]))

    elif direction == 'R':
        new_columns_needed = new_x - len(dig_grid[0]) + 1
        for _ in range(new_columns_needed):
            for i in range(len(dig_grid)):
                dig_grid[i].append('.')

    elif direction == 'L':
        new_columns_needed = abs(new_x)
        for _ in range(new_columns_needed):
            for i in range(len(dig_grid)):
                dig_grid[i].insert(0, '.')

    return dig_grid


def dig_instruction(dig_grid: list[list[str]], current_position: tuple[int, int], instruction: tuple[str, int, str]) -> tuple[list[list[str]], tuple[int, int]]:
    direction, steps, _ = instruction
    delta_x, delta_y = DIRECTION_MAP[direction]
    x, y = current_position
    
    for _ in range(steps):
        dig_grid[y][x] = '#'
        x += delta_x
        y += delta_y
    
    return dig_grid, (x, y)


def dig_trench(dig_plan: list[tuple[str, int, str]]) -> list[list[str]]:
    dig_grid = [['.']]
    current_position = (0, 0)
    
    for instruction in dig_plan:
        direction, steps, _ = instruction
        delta_x, delta_y = DIRECTION_MAP[direction]
        new_x = current_position[0] + delta_x * steps
        new_y = current_position[1] + delta_y * steps
        
        if not instruction_fits_inside_grid(dig_grid, new_x, new_y):

            offset_x = 0
            offset_y = 0
            if direction == 'L' and new_x < 0:
                offset_x = abs(new_x)
            elif direction == 'U' and new_y < 0:
                offset_y = abs(new_y)
                
            dig_grid = extend_grid(dig_grid, direction, new_x, new_y)
            current_position = (current_position[0] + offset_x, current_position[1] + offset_y)
        
        dig_grid, current_position = dig_instruction(dig_grid, current_position, instruction)

    return dig_grid


def dig_inside(dig_grid: list[list[str]]) -> list[list[str]]:
    height = len(dig_grid)
    width = len(dig_grid[0])
    visited = set()
    queue = deque()
    
    for y in range(height):
        for x in range(width):
            if (y == 0 or y == height - 1 or x == 0 or x == width - 1) and dig_grid[y][x] != '#':
                queue.append((x, y))
                visited.add((x, y))
                dig_grid[y][x] = 'O'
    
    while queue:
        x, y = queue.popleft()
        for delta_x, delta_y in DIRECTION_MAP.values():
            new_x, new_y = x + delta_x, y + delta_y
            if 0 <= new_x < width and 0 <= new_y < height and (new_x, new_y) not in visited and dig_grid[new_y][new_x] != '#':
                visited.add((new_x, new_y))
                dig_grid[new_y][new_x] = 'O'
                queue.append((new_x, new_y))
    
    for y in range(height):
        for x in range(width):
            if dig_grid[y][x] == '.':
                dig_grid[y][x] = '#'
    
    return dig_grid


def count_cubic_meters(dig_plan: list[tuple[str, int, str]]) -> int:
    dig_grid = dig_trench(dig_plan)
    dig_grid = dig_inside(dig_grid)
    return sum(Counter(line)['#'] for line in dig_grid)


def parse_hex_instructions(dig_plan: list[tuple[str, int, str]]) -> list[tuple[int, str]]:
    hex_instructions = []
    for instruction in dig_plan:
        hex_part = instruction[2].split('#')[1].split(')')[0]
        steps = int(hex_part[:5], 16)
        direction = HEX_DIRECTION_MAP[hex_part[-1]]
        hex_instructions.append((steps, direction))
    return hex_instructions


def count_vertices(hex_instructions: list[tuple[int, str]]) -> tuple[list[tuple[int, int]], int]:
    vertices = [(0,0)]
    steps_length = 0
    for instruction in hex_instructions:
        steps, direction = instruction
        steps_length += steps
        delta_x, delta_y = DIRECTION_MAP[direction]
        new_x = vertices[-1][0] + delta_x * steps
        new_y = vertices[-1][1] + delta_y * steps
        vertices.append((new_x, new_y))
    return vertices, steps_length
        

def count_hex_cubic_meters(dig_plan: list[tuple[str, int, str]]) -> int:
    hex_instructions = parse_hex_instructions(dig_plan)
    vertices, steps_length = count_vertices(hex_instructions)
    area = maths.polygon_area_with_boundary(vertices, steps_length)
    return area


def main() -> None:
    dig_plan = get_dig_plan()
    cubic_meters = count_cubic_meters(dig_plan)
    hex_cubic_meters = count_hex_cubic_meters(dig_plan)
    
    print(f"1. The number of cubic meters of lava is equal to: {cubic_meters}")
    print(f"2. The number of cubic meters of lava using hex instructions is equal to: {hex_cubic_meters}")


if __name__ == "__main__":
    main()