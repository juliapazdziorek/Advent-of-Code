from collections import deque
from utils import files

PIPE_MAP = {
    '|': ['N', 'S'],
    '-': ['W', 'E'],
    'L': ['N', 'E'],
    'J': ['N', 'W'],
    '7': ['S', 'W'],
    'F': ['S', 'E']
}

DIRECTION_MAP = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

SCALE_UP_PIPES_MAP = {
    '.': [['.', '.', '.'], ['.', '@', '.'], ['.', '.', '.']],
    '|': [['.', '|', '.'], ['.', '|', '.'], ['.', '|', '.']],
    '-': [['.', '.', '.'], ['-', '-', '-'], ['.', '.', '.']],
    'L': [['.', '|', '.'], ['.', 'L', '-'], ['.', '.', '.']],
    'J': [['.', '|', '.'], ['-', 'J', '.'], ['.', '.', '.']],
    '7': [['.', '.', '.'], ['-', '7', '.'], ['.', '|', '.']],
    'F': [['.', '.', '.'], ['.', 'F', '-'], ['.', '|', '.']]
}


def find_s_coordinates(pipe_array: list[list[str]]) -> tuple[int, int] | None:
    for i, row in enumerate(pipe_array):
        for j, val in enumerate(row):
            if val == 'S':
                return i, j
    return None


def get_pipe_direction(pipe: str, direction: str) -> str:
    return PIPE_MAP[pipe][1] if direction == PIPE_MAP[pipe][0] else PIPE_MAP[pipe][0]


def switch_direction(direction: str) -> str:
    return {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]


def new_pipe_possible(new_pipe: str, enter_direction: str) -> bool:
    if new_pipe == 'S':
        return True
    return enter_direction in PIPE_MAP[new_pipe]


def get_new_position(pipe: str, direction: str, coordinates: tuple[int, int], pipe_array: list[list[str]]) -> tuple[tuple[int, int], str, str] | None:
    direction = get_pipe_direction(pipe, direction) if pipe != 'S' else direction
    delta_i, delta_j = DIRECTION_MAP[direction]
    new_i, new_j = coordinates[0] + delta_i, coordinates[1] + delta_j

    if not (0 <= new_i < len(pipe_array) and 0 <= new_j < len(pipe_array[0])):
        return None
    
    new_pipe = pipe_array[new_i][new_j]
    if new_pipe == '.':
        return None
    
    new_direction = switch_direction(direction)
    if new_pipe_possible(new_pipe, new_direction):
        return (new_i, new_j), new_pipe, new_direction
    return None


def find_loop(pipe_array: list[list[str]], coordinates: tuple[int, int], direction: str) -> set[tuple[int, int]] | None:
    pipe = pipe_array[coordinates[0]][coordinates[1]]
    loop_coordinates: set[tuple[int, int]] = set()

    while True:
        loop_coordinates.add((coordinates[0], coordinates[1]))
        new_position = get_new_position(pipe, direction, coordinates, pipe_array)

        if new_position is None:
            return None
        
        coordinates, pipe, direction = new_position

        if pipe == 'S' and len(loop_coordinates) != 0:
            loop_coordinates.add((coordinates[0], coordinates[1]))
            return loop_coordinates


def get_loop_coordinates(pipe_array: list[list[str]]) -> set[tuple[int, int]] | None:
    s_coordinates = find_s_coordinates(pipe_array)

    if s_coordinates is None:
        return None
    
    for direction in ['N', 'E', 'S', 'W']:
        loop_coordinates = find_loop(pipe_array, s_coordinates, direction)
        if loop_coordinates is not None:
            return loop_coordinates
    return None


def count_steps_farthest_point(loop_coordinates: set[tuple[int, int]]) -> int:
    return len(loop_coordinates) // 2


def mark_not_loop(pipe_array: list[list[str]], loop_coordinates: set[tuple[int, int]]) -> list[list[str]]:
    for i, row in enumerate(pipe_array):
        for j in range(len(row)):
            if (i, j) not in loop_coordinates:
                pipe_array[i][j] = '.'
    return pipe_array


def replace_s(pipe_array: list[list[str]]) -> list[list[str]]:
    s_coordinates = find_s_coordinates(pipe_array)

    if s_coordinates is None:
        return pipe_array
    
    i, j = s_coordinates
    neighbors = []
    for direction, (delta_i, delta_j) in DIRECTION_MAP.items():
        new_i, new_j = i + delta_i, j + delta_j

        if 0 <= new_i < len(pipe_array) and 0 <= new_j < len(pipe_array[0]):
            neighbor = pipe_array[new_i][new_j]

            if neighbor != '.' and switch_direction(direction) in PIPE_MAP.get(neighbor, []):
                neighbors.append(direction)

    for pipe, directions in PIPE_MAP.items():
        if set(directions) == set(neighbors):
            pipe_array[i][j] = pipe
            break
    return pipe_array


def scale_up_array(pipe_array: list[list[str]]) -> list[list[str]]:
    rows, columns = len(pipe_array), len(pipe_array[0])
    new_pipe_array = [['.' for _ in range(columns * 3)] for _ in range(rows * 3)]

    for row in range(rows):
        for col in range(columns):
            pipe = pipe_array[row][col]
            for i in range(3):
                for j in range(3):
                    new_pipe_array[row * 3 + i][col * 3 + j] = SCALE_UP_PIPES_MAP[pipe][i][j]
    return new_pipe_array


def mark_loop(pipe_array: list[list[str]]) -> list[list[str]]:
    for row in pipe_array:
        for j in range(len(row)):
            if row[j] != '.' and row[j] != '@':
                row[j] = '#'
    return pipe_array


def flood_array(pipe_array: list[list[str]]) -> list[list[str]]:
    rows, columns = len(pipe_array), len(pipe_array[0])
    visited = set()
    queue = deque()

    for i in range(rows):
        for j in [0, columns - 1]:
            if pipe_array[i][j] != '#':
                queue.append((i, j))
                visited.add((i, j))
    for j in range(columns):
        for i in [0, rows - 1]:
            if pipe_array[i][j] != '#':
                queue.append((i, j))
                visited.add((i, j))

    while queue:
        i, j = queue.popleft()
        if pipe_array[i][j] == '#':
            continue
        pipe_array[i][j] = '#'
        
        for delta_i, delta_j in DIRECTIONS:
            new_i, new_j = i + delta_i, j + delta_j
            if 0 <= new_i < rows and 0 <= new_j < columns and (new_i, new_j) not in visited and pipe_array[new_i][new_j] != '#':
                queue.append((new_i, new_j))
                visited.add((new_i, new_j))
    return pipe_array


def modify_pipe_array(pipe_array: list[list[str]], loop_coordinates: set[tuple[int, int]]) -> list[list[str]]:
    pipe_array = mark_not_loop(pipe_array, loop_coordinates)
    pipe_array = replace_s(pipe_array)
    pipe_array = scale_up_array(pipe_array)
    pipe_array = mark_loop(pipe_array)
    pipe_array = flood_array(pipe_array)
    return pipe_array


def count_spaces_inside_loop(pipe_array: list[list[str]]) -> int:
    return sum(row.count('@') for row in pipe_array)


def main() -> None:
    pipe_array = files.read_file_into_2d_array('data.txt')
    loop_coordinates = get_loop_coordinates(pipe_array)
    if loop_coordinates is None:
        print("No loop found.")
        return
    
    steps_to_farthest_point = count_steps_farthest_point(loop_coordinates)
    pipe_array = modify_pipe_array(pipe_array, loop_coordinates)
    spaces_inside_loop = count_spaces_inside_loop(pipe_array)

    print(f"1. The numbers of steps to farthest the point from the starting position is equal to: {steps_to_farthest_point}")
    print(f"2. The number of spaces between the loop is equal to: {spaces_inside_loop}")


if __name__ == "__main__":
    main()