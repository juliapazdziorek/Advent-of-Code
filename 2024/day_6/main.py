from utils import files

# Day 6: Guard Gallivant
# https://adventofcode.com/2024/day/6


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_guard_position(grid: list[list[str]]) -> tuple[int, int]:
    return next((i, j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == '^')


def mark_walked_on_positions(grid: list[list[str]]) -> list[list[str]]:
    guard_position = get_guard_position(grid)
    marked_grid = [row.copy() for row in grid]
    direction_i = 0
    marked_grid[guard_position[0]][guard_position[1]] = 'X'

    while 0 <= guard_position[0] < len(marked_grid) and 0 <= guard_position[1] < len(marked_grid[0]):
        next_position = (guard_position[0] + DIRECTIONS[direction_i][0], guard_position[1] + DIRECTIONS[direction_i][1])
        if not (0 <= next_position[0] < len(marked_grid) and 0 <= next_position[1] < len(marked_grid[0])):
            break

        if marked_grid[next_position[0]][next_position[1]] == '#':
            direction_i = (direction_i + 1) % len(DIRECTIONS)
            continue

        guard_position = next_position
        if marked_grid[guard_position[0]][guard_position[1]] in '.':
            marked_grid[guard_position[0]][guard_position[1]] = 'X'

    return marked_grid


def count_x(grid: list[list[str]]) -> int:
    return sum(1 for i in grid for position in i if position == 'X')


def count_distinct_positions(grid: list[list[str]]) -> int:
    marked_grid = mark_walked_on_positions(grid)
    return count_x(marked_grid)


def get_x_positions(marked_grid: list[list[str]]) -> list[tuple[int, int]]:
    return [(i, j) for i in range(len(marked_grid)) for j in range(len(marked_grid[i])) if marked_grid[i][j] == 'X']


def creates_loop(guard_position: tuple[int, int], x_position: tuple[int, int], grid: list[list[str]]) -> bool:
    new_obstruction_grid = [row.copy() for row in grid]
    new_obstruction_grid[x_position[0]][x_position[1]] = '#'
    new_obstruction_grid[guard_position[0]][guard_position[1]] = '.'
    direction_i = 0
    visited = set()

    while 0 <= guard_position[0] < len(new_obstruction_grid) and 0 <= guard_position[1] < len(new_obstruction_grid[0]):
        state = (guard_position[0], guard_position[1], direction_i)
        if state in visited:
            return True
        visited.add(state)

        next_position = (guard_position[0] + DIRECTIONS[direction_i][0], guard_position[1] + DIRECTIONS[direction_i][1])
        if not (0 <= next_position[0] < len(new_obstruction_grid) and 0 <= next_position[1] < len(new_obstruction_grid[0])):
            break

        if new_obstruction_grid[next_position[0]][next_position[1]] == '#':
            direction_i = (direction_i + 1) % len(DIRECTIONS)
            continue

        guard_position = next_position

    return False


def count_loop_positions(grid: list[list[str]]) -> int:
    marked_grid = mark_walked_on_positions(grid)
    x_positions = get_x_positions(marked_grid)
    guard_position = get_guard_position(grid)
    return sum(1 for x_position in x_positions if creates_loop(guard_position, x_position, grid))


def main() -> None:
    grid = files.read_file_into_2d_array('data.txt')
    distinct_positions = count_distinct_positions(grid)
    loop_positions = count_loop_positions(grid)

    print(f"1. The number distinct positions is equal to: {distinct_positions}")
    print(f"2. The number new obstruction positions that will create a loop positions is equal to: {loop_positions}")


if __name__ == "__main__":
    main()