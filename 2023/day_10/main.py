from utils import files


# Day 10: Pipe Maze
# https://adventofcode.com/2023/day/10


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


def find_s_coordinates(pipe_array):
    s_coordinates = []

    i = 0 
    while i < len(pipe_array):
        j = 0
        while j < len(pipe_array[i]):
            if pipe_array[i][j] == 'S':
                s_coordinates = [i, j]
                break

            j += 1
        i += 1
    return s_coordinates


def get_direction(pipe, direction):
    return PIPE_MAP[pipe][1] if direction == PIPE_MAP[pipe][0] else PIPE_MAP[pipe][0]


def switch_direction(direction):
    return {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]


def new_pipe_possible(new_pipe, enter_direction):
    return enter_direction in PIPE_MAP[new_pipe] if new_pipe != 'S' else enter_direction


def direction_possible(pipe, direction, coordinates, pipe_array):
    direction = get_direction(pipe, direction) if pipe != 'S' else direction
    delta_i, delta_j = DIRECTION_MAP[direction]
    new_i = coordinates[0] + delta_i
    new_j = coordinates[1] + delta_j

    if new_i < 0 or new_i >= len(pipe_array) or new_j < 0 or new_j >= len(pipe_array[new_i]):
        return False

    new_pipe = pipe_array[new_i][new_j]
    if new_pipe == '.':
        return False

    enter_direction = switch_direction(direction)
    if new_pipe_possible(new_pipe, enter_direction):
        return [new_i, new_j], new_pipe, enter_direction
    return False


def count_steps_in_loop(pipe_array: list[list[str]], coordinates: list[int], direction: str) -> int | None:
    steps = 0
    pipe = pipe_array[coordinates[0]][coordinates[1]]
    while True:
        result = direction_possible(pipe, direction, coordinates, pipe_array)
        if not result:
            return None
        coordinates, pipe, direction = result
        steps += 1
        
        if pipe == 'S' and steps != 0:
            break

    return steps
    

def get_farthest_point(pipe_array):
    s_coordinates = find_s_coordinates(pipe_array)
    for direction in ['N', 'E', 'S', 'W']:
        steps = count_steps_in_loop(pipe_array, s_coordinates, direction)

        if steps is None:
            continue
        else:
            return steps / 2
    return 0
        

def main() -> None:
    pipe_array = files.read_file_into_2d_array('data.txt')
    steps_to_farthest_point = int(get_farthest_point(pipe_array))

    print(f"1. The numbers of steps to point farthest from the starting position is equal to: {steps_to_farthest_point}")
    #print(f"2. The answer to part 2 is equal to: {0}")


if __name__ == "__main__":
    main()