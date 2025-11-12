from utils import files

# Day 4: Ceres Search
# https://adventofcode.com/2024/day/4


XMAS = ['X', 'M', 'A', 'S']

DIRECTIONS = [(1, 1), (1, 0), (1, -1),
              (0, 1), (0, -1),
              (-1, 1), (-1, 0), (-1, -1)]


def find_x_coordinates(grid: list[list[str]]) -> list[tuple[int,int]]:
    return [(i, j) for i, row in enumerate(grid) for j, char in enumerate(row) if char == XMAS[0]]


def check_xmas(x_coordinates: tuple[int,int], grid: list[list[str]]) -> int:
    matches = 0
    for directions_i, directions_j in DIRECTIONS:
        new_coordinates = x_coordinates

        for letter in XMAS[1:]:
            new_coordinates = (new_coordinates[0] + directions_i, new_coordinates[1] + directions_j)
            if 0 <= new_coordinates[0] < len(grid) and 0 <= new_coordinates[1] < len(grid[0]):
                if grid[new_coordinates[0]][new_coordinates[1]] == letter:
                    if letter == XMAS[-1]:
                        matches += 1
                else:
                    break
            else:
                break
    return matches


def count_xmas(grid: list[list[str]]) -> int:
    x_coordinates = find_x_coordinates(grid)
    return sum(check_xmas(coordinates, grid) for coordinates in x_coordinates)


def find_mas_coordinates(grid: list[list[str]]) -> list[tuple[int,int]]:
    return [(i, j) for i, row in enumerate(grid) for j, char in enumerate(row) if char == XMAS[2]]


def check_x_mas(x_coordinates: tuple[int,int], grid: list[list[str]]) -> int:
    new_coordinates = x_coordinates
    if not (1 <= new_coordinates[0] < len(grid) - 1 and 1 <= new_coordinates[1] < len(grid[0]) - 1):
        return 0

    upper_left = grid[new_coordinates[0] - 1][new_coordinates[1] - 1]
    upper_right = grid[new_coordinates[0] - 1][new_coordinates[1] + 1]
    bottom_left = grid[new_coordinates[0] + 1][new_coordinates[1] - 1]
    bottom_right = grid[new_coordinates[0] + 1][new_coordinates[1] + 1]

    required = {XMAS[1], XMAS[-1]}
    first_diagonal_valid = {upper_left, bottom_right} == required
    second_diagonal_valid = {upper_right, bottom_left} == required

    return 1 if first_diagonal_valid and second_diagonal_valid else 0


def count_x_mas(grid: list[list[str]]) -> int:
    mas_coordinates = find_mas_coordinates(grid)
    return sum(check_x_mas(coordinates, grid) for coordinates in mas_coordinates)


def main() -> None:
    grid = files.read_file_into_2d_array('data.txt')
    number_of_xmas = count_xmas(grid)
    number_of_x_mas = count_x_mas(grid)

    print(f"1. The number of xmas is equal to: {number_of_xmas}")
    print(f"2. The number of x-mas is equal to: {number_of_x_mas}")



if __name__ == "__main__":
    main()
