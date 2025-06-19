from collections import deque
import math
from utils import files


# Day 8: Haunted Wasteland
# https://adventofcode.com/2023/day/8


def get_data() -> tuple[list[int], dict[str, list[str]], list[str]]:
    lines = files.read_file('data.txt')

    instructions_line = 0
    for i, line in enumerate(lines):
        if not line.strip():
            instructions_line = i
            break

    instructions = [0 if char == 'L' else 1 for char in ''.join(lines[:instructions_line]) if char in 'LR']

    mapping = {}
    starting_symbols = []
    for line in lines[instructions_line + 1:]:
        if not line.strip():
            continue
        key, rest = line.split(' = ')
        left, right = rest.strip('()').split(', ')
        mapping[key] = [left, right]

        if line[2] == 'A':
            starting_symbols.append(key)

    return instructions, mapping, starting_symbols


def count_steps(instructions: list[int], mapping: dict[str, list[str]], start_symbol: str='AAA', end_symbol_ending: str='ZZZ') -> int:
    current_symbol = start_symbol
    current_instructions = deque(instructions)
    steps = 0
    continue_search = True

    while continue_search:

        if len(current_instructions) == 0:
            current_instructions.extend(instructions)

        instruction = current_instructions.popleft()
        current_symbol = mapping[current_symbol][instruction]
        steps += 1

        if current_symbol.endswith(end_symbol_ending):
            continue_search = False
    return steps


def find_cycle_length(start_symbol: str, instructions: list[int], mapping: dict[str, list[str]]) -> int:
    return count_steps(instructions, mapping, start_symbol, 'Z')


def count_steps_simultaneously(instructions: list[int], mapping: dict[str, list[str]], starting_symbols: list[str]) -> int:
    cycle_lengths = [find_cycle_length(symbol, instructions, mapping) for symbol in starting_symbols]
    steps = math.lcm(*cycle_lengths)
    return steps


def main() -> None:
    instructions, mapping, starting_symbols = get_data()
    steps = count_steps(instructions, mapping)
    steps_simultaneously = count_steps_simultaneously(instructions, mapping, starting_symbols)
    print(f"1. The number of steps required to reach 'ZZZ' is equal to: {steps}")
    print(f"2. The number of steps required to reach all finish points simultaneously is equal to: {steps_simultaneously}")


if __name__ == "__main__":
    main()