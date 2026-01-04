from utils import files

# Day 4: Printing Department
# https://adventofcode.com/2025/day/4


ADJACENT_POSITIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def find_rolls_positions(grid: list[list[str]]) -> list[tuple[int, int]]:
    rolls_positions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '@':
                rolls_positions.append((i,j))

    return rolls_positions


def check_if_accessible(grid: list[list[str]], roll: tuple[int, int]) -> bool:
    adjacent_rolls = 0
    for position in ADJACENT_POSITIONS:
        new_position = (roll[0] + position[0], roll[1] + position[1])
        if 0 <= new_position[0] < len(grid) and 0 <= new_position[1] < len(grid[0]):
            if grid[new_position[0]][new_position[1]] == '@':
                adjacent_rolls += 1
            if adjacent_rolls >= 4:
                return False
            
    return True


def count_rolls_accessed(grid: list[list[str]]) -> int:
    rolls_positions = find_rolls_positions(grid)
    return sum([1 for roll in rolls_positions if check_if_accessible(grid, roll)])


def find_accessible_rolls_positions(grid: list[list[str]]) -> list[tuple[int, int]]:
    rolls_positions = find_rolls_positions(grid)
    return [roll for roll in rolls_positions if check_if_accessible(grid, roll)]


def count_rolls_removed(grid: list[list[str]]) -> int:
    grid = [row.copy() for row in grid]
    removed_rolls = 0

    while accessible_rolls_positions := find_accessible_rolls_positions(grid):
        for roll in accessible_rolls_positions:
            removed_rolls += 1
            grid[roll[0]][roll[1]] = '.'

    return removed_rolls

                
def main() -> None:
    grid = files.read_file_into_2d_array('data.txt')
    rolls_accessed = count_rolls_accessed(grid)
    rolls_removed = count_rolls_removed(grid)

    print(f"1. The number of paper rolls that can be accessed is equal to: {rolls_accessed}")
    print(f"2. The number of paper rolls that can be removed is equal to: {rolls_removed}")


if __name__ == "__main__":
    main()