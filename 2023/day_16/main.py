from utils import files
from collections import deque


# Day 16: The Floor Will Be Lava
# https://adventofcode.com/2023/day/16


DIRECTION_MAP = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1)
}

MIRROR_REFLECTIONS = {
    '/': {'R': 'U', 'U': 'R', 'L': 'D', 'D': 'L'},
    '\\': {'R': 'D', 'D': 'R', 'L': 'U', 'U': 'L'}
}


def move(y: int, x: int, direction: str) -> tuple[int, int]:
    delta_y, delta_x = DIRECTION_MAP[direction]
    return y + delta_y, x + delta_x


def get_next_positions(y: int, x: int, direction: str, tile: str) -> list[tuple[int, int, str]]:
    if tile == '.':
        new_y, new_x = move(y, x, direction)
        return [(new_y, new_x, direction)]
    
    elif tile in ['/', '\\']:
        new_direction = MIRROR_REFLECTIONS[tile][direction]
        new_y, new_x = move(y, x, new_direction)
        return [(new_y, new_x, new_direction)]
    
    elif tile == '-':
        if direction in ['U', 'D']:
            left_y, left_x = move(y, x, 'L')
            right_y, right_x = move(y, x, 'R')
            return [(left_y, left_x, 'L'), (right_y, right_x, 'R')]
        else:
            new_y, new_x = move(y, x, direction)
            return [(new_y, new_x, direction)]
    
    elif tile == '|':
        if direction in ['L', 'R']:
            up_y, up_x = move(y, x, 'U')
            down_y, down_x = move(y, x, 'D')
            return [(up_y, up_x, 'U'), (down_y, down_x, 'D')]
        else:
            new_y, new_x = move(y, x, direction)
            return [(new_y, new_x, direction)]
    
    return []


def count_energized_tiles(tile_grid: list[list[str]], start: tuple[int, int, str]=(0, 0, 'R')) -> int:
    energized = set()
    visited = set()
    queue = deque([start])

    while queue:
        y, x, direction = queue.popleft()
        
        if (y < 0 or y >= len(tile_grid) or 
            x < 0 or x >= len(tile_grid[0]) or 
            (y, x, direction) in visited):
            continue
        
        visited.add((y, x, direction))
        energized.add((y, x))
        
        tile = tile_grid[y][x]
        next_positions = get_next_positions(y, x, direction, tile)
        for next_y, next_x, next_direction in next_positions:
            queue.append((next_y, next_x, next_direction))
    
    return len(energized)


def count_max_energized_tiles(tile_grid: list[list[str]]) -> int:
    max_energized = 0
    height, width = len(tile_grid), len(tile_grid[0])
    
    for x in range(width):
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (0, x, 'D')))
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (height - 1, x, 'U')))
    for y in range(height):
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (y, 0, 'R')))
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (y, width - 1, 'L')))
    
    return max_energized


def main() -> None:
    tile_grid = files.read_file_into_2d_array('data.txt')
    energized_tiles = count_energized_tiles(tile_grid)
    max_energized_tiles = count_max_energized_tiles(tile_grid)

    print(f"1. The number of energized tiles is equal to: {energized_tiles}")
    print(f"2. The number of the largest number of energized tiles is equal to: {max_energized_tiles}")


if __name__ == "__main__":
    main()