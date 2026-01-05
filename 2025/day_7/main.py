from utils import files

# Day 7: Laboratories
# https://adventofcode.com/2025/day/7


def find_s(grid: list[list[str]]) -> int:
    for i, char in enumerate(grid[0]):
        if char == 'S':
            return i
    return 0


def count_splits(grid: list[list[str]]) -> int:
    search_coordinates = [(find_s(grid), 0)]
    splits = 0
    visited = set()
    
    while search_coordinates:
        coordinates = search_coordinates.pop(0)
        
        if coordinates in visited:
            continue
        visited.add(coordinates)
        
        while coordinates[1] + 1 < len(grid):
            coordinates = (coordinates[0], coordinates[1] + 1)
            
            if coordinates in visited:
                break
            visited.add(coordinates)
            
            if grid[coordinates[1]][coordinates[0]] == '^':
                splits += 1
                if coordinates[0] - 1 >= 0:
                    search_coordinates.append((coordinates[0] - 1, coordinates[1]))
                if coordinates[0] + 1 < len(grid[0]):
                    search_coordinates.append((coordinates[0] + 1, coordinates[1]))
                break
                
    return splits


def count_timelines(grid: list[list[str]], coordinates: tuple[int, int], memo: dict = None) -> int:
    if memo is None:
        memo = {}
    
    if coordinates in memo:
        return memo[coordinates]
    
    if coordinates[1] == len(grid):
        return 1

    result = 0
    if grid[coordinates[1]][coordinates[0]] == '^':
        if coordinates[0] - 1 >= 0:
            result += count_timelines(grid, (coordinates[0] - 1, coordinates[1]), memo)
        if coordinates[0] + 1 < len(grid[0]):
            result += count_timelines(grid, (coordinates[0] + 1, coordinates[1]), memo)
    else:
        result += count_timelines(grid, (coordinates[0], coordinates[1] + 1), memo)
    
    memo[coordinates] = result
    return result


def main() -> None:
    grid = files.read_file_into_2d_array('data.txt')
    splits = count_splits(grid)
    timelines = count_timelines(grid, (find_s(grid), 0))

    print(f"1. The number of beam splits is equal to: {splits}")
    print(f"2. The number of different timelines is equal to: {timelines}")


if __name__ == "__main__":
    main()