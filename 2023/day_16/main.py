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


def move(x: int, y: int, direction: str) -> tuple[int, int]:
    delta_x, delta_y = DIRECTION_MAP[direction]
    return x + delta_x, y + delta_y


def get_next_positions(x: int, y: int, direction: str, tile: str) -> list[tuple[int, int, str]]:
    if tile == '.':
        new_x, new_y = move(x, y, direction)
        return [(new_x, new_y, direction)]
    
    elif tile in ['/', '\\']:
        new_direction = MIRROR_REFLECTIONS[tile][direction]
        new_x, new_y = move(x, y, new_direction)
        return [(new_x, new_y, new_direction)]
    
    elif tile == '-':
        if direction in ['U', 'D']:
            left_x, left_y = move(x, y, 'L')
            right_x, right_y = move(x, y, 'R')
            return [(left_x, left_y, 'L'), (right_x, right_y, 'R')]
        else:
            new_x, new_y = move(x, y, direction)
            return [(new_x, new_y, direction)]
    
    elif tile == '|':
        if direction in ['L', 'R']:
            up_x, up_y = move(x, y, 'U')
            down_x, down_y = move(x, y, 'D')
            return [(up_x, up_y, 'U'), (down_x, down_y, 'D')]
        else:
            new_x, new_y = move(x, y, direction)
            return [(new_x, new_y, direction)]
    
    return []


def count_energized_tiles(tile_grid: list[list[str]], start: tuple[int, int, str]=(0, 0, 'R')) -> int:
    energized = set()
    visited = set()
    queue = deque([start])

    while queue:
        x, y, direction = queue.popleft()
        
        if (x < 0 or x >= len(tile_grid) or 
            y < 0 or y >= len(tile_grid[0]) or 
            (x, y, direction) in visited):
            continue
        
        visited.add((x, y, direction))
        energized.add((x, y))
        
        tile = tile_grid[x][y]
        next_positions = get_next_positions(x, y, direction, tile)
        for next_x, next_y, next_direction in next_positions:
            queue.append((next_x, next_y, next_direction))
    
    return len(energized)


def count_max_energized_tiles(tile_grid: list[list[str]]) -> int:
    max_energized = 0
    height, width = len(tile_grid), len(tile_grid[0])
    
    for i in range(width):
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (0, i, 'D')))
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (height - 1, i, 'U')))
    for i in range(height):
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (i, 0, 'R')))
        max_energized = max(max_energized, count_energized_tiles(tile_grid, (i, width - 1, 'L')))
    
    return max_energized


def main() -> None:
    tile_grid = files.read_file_into_2d_array('data.txt')
    energized_tiles = count_energized_tiles(tile_grid)
    max_energized_tiles = count_max_energized_tiles(tile_grid)

    print(f"1. The number of energized tiles is equal to: {energized_tiles}")
    print(f"2. The number of the largest number of energized tiles is equal to: {max_energized_tiles}")


if __name__ == "__main__":
    main()