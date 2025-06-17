from dataclasses import dataclass
from typing import Optional
import math

from utils import files


# Day 3: Gear Ratios
# https://adventofcode.com/2023/day/3


@dataclass
class PartNumber:
    value: int
    indexes: list[int]


def is_symbol(char: str) -> bool:
    return not char.isdigit() and char != '.'


def is_part_number(row_index: int, num_indexes: list[int], array: list[list[str]]) -> bool:
    for col_index in num_indexes:
        for delta_row in [-1, 0, 1]:
            for delta_col in [-1, 0, 1]:
                if delta_row == 0 and delta_col == 0:
                    continue
                new_row = row_index + delta_row
                new_col = col_index + delta_col
                if 0 <= new_row < len(array) and 0 <= new_col < len(array[new_row]):
                    if is_symbol(array[new_row][new_col]):
                        return True
    return False


def find_part_numbers(array: list[list[str]]) -> list[PartNumber]:
    part_numbers: list[PartNumber] = []

    for row_index, row in enumerate(array):
        col_index = 0
        while col_index < len(row):
            if row[col_index].isdigit():
                digits = []
                digit_indexes = []
                while col_index < len(row) and row[col_index].isdigit():
                    digits.append(row[col_index])
                    digit_indexes.append(col_index)
                    col_index += 1

                if is_part_number(row_index, digit_indexes, array):
                    part_numbers.append(PartNumber(int("".join(digits)), digit_indexes))
            else:
                col_index += 1

    return part_numbers


@dataclass
class Gear:
    adjacent_numbers: list[int]

    def count_ratio(self) -> int:
        return math.prod(self.adjacent_numbers)

    @property
    def ratio(self) -> int:
        return self.count_ratio()


def try_to_create_gear(col_index: int, row_index: int, array: list[list[str]]) -> Optional[Gear]:
    positions_to_check: list[tuple[int, int]] = []

    for delta_row in [-1, 0, 1]:
        for delta_col in [-1, 0, 1]:
            if delta_row == 0 and delta_col == 0:
                continue
            new_row = row_index + delta_row
            new_col = col_index + delta_col
            if 0 <= new_row < len(array) and 0 <= new_col < len(array[new_row]):
                positions_to_check.append((new_row, new_col))

    found_positions: list[tuple[int, int]] = []
    part_numbers: list[int] = []

    for row, col in positions_to_check:
        if array[row][col].isdigit() and (row, col) not in found_positions:
            line = array[row]
            start = col
            end = col

            while start > 0 and line[start - 1].isdigit():
                start -= 1
            while end < len(line) - 1 and line[end + 1].isdigit():
                end += 1

            number = int(''.join(line[start:end + 1]))
            for i in range(start, end + 1):
                found_positions.append((row, i))
            part_numbers.append(number)

    if len(part_numbers) == 2:
        return Gear(part_numbers)
    return None


def find_gears(array: list[list[str]]) -> list[Gear]:
    gears: list[Gear] = []

    for row_index, row in enumerate(array):
        for col_index, char in enumerate(row):
            if char == '*':
                gear = try_to_create_gear(col_index, row_index, array)
                if gear is not None:
                    gears.append(gear)

    return gears


def count_sums() -> tuple[int, int]:
    array = files.read_file_into_2d_array('data.txt')

    part_numbers = find_part_numbers(array)
    gears = find_gears(array)

    sum_of_part_numbers = sum(p.value for p in part_numbers)
    sum_of_gear_ratios = sum(g.ratio for g in gears)

    return sum_of_part_numbers, sum_of_gear_ratios


def main() -> None:
    sum_parts, sum_gears = count_sums()
    print(f"1. The sum of part numbers is equal to {sum_parts}")
    print(f"2. The sum of gear ratios is equal to {sum_gears}")


if __name__ == "__main__":
    main()
