import re
from collections.abc import Callable
from utils import files


# Day 3: Mull It Over
# https://adventofcode.com/2024/day/3


def get_muls(lines: list[str]) -> list[str]:
    pattern = r'mul\(\d{1,3},\d{1,3}\)'
    muls = [re.findall(pattern, line) for line in lines]
    return [mul for sublist in muls for mul in sublist]


def get_mules_enables(lines: list[str]) -> list[str]:
    pattern = r'mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)'
    instructions_lines = [re.findall(pattern, line) for line in lines]

    muls = []
    enabled = True
    for instruction_line in instructions_lines:
        for instruction in instruction_line:
            if instruction == 'do()':
                enabled = True
            elif instruction == 'don\'t()':
                enabled = False
            elif enabled:
                muls.append(instruction)
    return muls


def count_mul(mul: str) -> int:
    nums =  re.findall(r'\d+', mul)
    return int(nums[0]) * int(nums[1])


def get_sum_of_muls(lines: list[str], get_mul_func: Callable[[list[str]], list[str]]) -> int:
    muls = get_mul_func(lines)
    results_of_muls = [count_mul(mul) for mul in muls]
    return sum(results_of_muls)


def main() -> None:
    lines = files.read_file('data.txt')
    sum_of_muls = get_sum_of_muls(lines, get_muls)
    sum_of_muls_enabled = get_sum_of_muls(lines, get_mules_enables)

    print(f"1. The sum of all mul operations is equal to: {sum_of_muls}")
    print(f"2. The sum of all enabled mul operations is equal to: {sum_of_muls_enabled}")


if __name__ == "__main__":
    main()