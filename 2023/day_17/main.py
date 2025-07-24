from typing import Optional, Callable
from utils import files
import heapq


# Day 17: Clumsy Crucible
# https://adventofcode.com/2023/day/17


DIRECTION_MAP = {
    'U': (-1, 0),
    'D': (1, 0),
    'R': (0, 1),
    'L': (0, -1),
}

TURNS_MAP = {
    'U': ['L', 'R'],
    'D': ['L', 'R'],    
    'L': ['U', 'D'],
    'R': ['U', 'D']
}


def get_valid_moves_normal_crucibles(y: int, x: int, direction: str, steps: int, heat_map: list[list[str]]) -> list[tuple[int, int, str, int, int]]:
    return get_valid_moves(y, x, direction, steps, heat_map, min_steps=1, max_steps=3)


def check_if_target(y: int, target_y: int, x: int, target_x: int, steps: int, min_steps: int = 1) -> bool:
    return y == target_y and x == target_x and steps >= min_steps


def check_if_target_normal_crucibles(y: int, target_y: int, x: int, target_x: int, steps: int) -> bool:
    return check_if_target(y, target_y, x, target_x, steps, min_steps=1)


def get_valid_moves_ultra_crucibles(y: int, x: int, direction: str, steps: int, heat_map: list[list[str]]) -> list[tuple[int, int, str, int, int]]:
    return get_valid_moves(y, x, direction, steps, heat_map, min_steps=4, max_steps=10)


def check_if_target_ultra_crucibles(y: int, target_y: int, x: int, target_x: int, steps: int) -> bool:
    return check_if_target(y, target_y, x, target_x, steps, min_steps=4)


def count_min_heat_loss(
    heat_map_array: list[list[str]], 
    get_valid_moves_func: Callable[[int, int, str, int, list[list[str]]], list[tuple[int, int, str, int, int]]], 
    check_target_func: Callable[[int, int, int, int, int], bool]
    ) -> Optional[int]:

    target_y, target_x = len(heat_map_array) - 1, len(heat_map_array[0]) - 1
    
    queue = []
    visited = set()
    heapq.heappush(queue, (0, 0, 0, 'R', 0))
    heapq.heappush(queue, (0, 0, 0, 'D', 0))

    while queue:
        current_heat, y, x, direction, steps = heapq.heappop(queue)
        
        state = (y, x, direction, steps)
        if state in visited:
            continue
        visited.add(state)
        
        if check_target_func(y, target_y, x, target_x, steps):
            return current_heat
        
        valid_moves = get_valid_moves_func(y, x, direction, steps, heat_map_array)
        
        for new_y, new_x, new_direction, new_steps, heat_cost in valid_moves:
            new_state = (new_y, new_x, new_direction, new_steps)
            if new_state not in visited:
                new_total_heat = current_heat + heat_cost
                heapq.heappush(queue, (new_total_heat, new_y, new_x, new_direction, new_steps))
    
    return None


def get_valid_moves(y: int, x: int, direction: str, steps: int, heat_map: list[list[str]], min_steps: int = 1, max_steps: int = 3) -> list[tuple[int, int, str, int, int]]:
    valid_moves = []

    if steps < max_steps:
        delta_y, delta_x = DIRECTION_MAP[direction]
        new_y, new_x = y + delta_y, x + delta_x
        
        if 0 <= new_y < len(heat_map) and 0 <= new_x < len(heat_map[0]):
            heat_cost = int(heat_map[new_y][new_x])
            valid_moves.append((new_y, new_x, direction, steps + 1, heat_cost))
    
    if steps >= min_steps:
        for new_direction in TURNS_MAP[direction]:
            delta_y, delta_x = DIRECTION_MAP[new_direction]
            new_y, new_x = y + delta_y, x + delta_x
            
            if 0 <= new_y < len(heat_map) and 0 <= new_x < len(heat_map[0]):
                heat_cost = int(heat_map[new_y][new_x])
                valid_moves.append((new_y, new_x, new_direction, 1, heat_cost))
    
    return valid_moves


def main() -> None:
    heat_map_array = files.read_file_into_2d_array('data.txt')
    min_heat_loss_normal_crucibles = count_min_heat_loss(heat_map_array, get_valid_moves_normal_crucibles, check_if_target_normal_crucibles)
    min_heat_loss_ultra_crucibles = count_min_heat_loss(heat_map_array, get_valid_moves_ultra_crucibles, check_if_target_ultra_crucibles)
    
    print(f"1. The minimal heat loss is equal to: {min_heat_loss_normal_crucibles}")
    print(f"2. The minimal heat loss using ultra crucibles is equal to: {min_heat_loss_ultra_crucibles}")

    
if __name__ == "__main__":
    main()