from utils import files
from utils import maths


# Day 14: Parabolic Reflector Dish
# https://adventofcode.com/2023/day/14


def transpose_2d_array(rock_array: list[list[str]]) -> list[list[str]]:
    return maths.transpose_2d_array(rock_array)


def tilt(rock_array: list[list[str]]) -> list[list[str]]:
    for row in rock_array:
        row_length = len(row)
        i = 0
        while i < row_length:
            if row[i] == '#':
                i += 1
                continue

            start = i
            o_count = 0
            while i < row_length and row[i] != '#':
                if row[i] == 'O':
                    o_count += 1
                i += 1
            end = i

            for j in range(start, end):
                if j - start < o_count:
                    row[j] = 'O'
                else:
                    row[j] = '.'

    return rock_array


def tilt_north(rock_array: list[list[str]]) -> list[list[str]]:
    rock_array = transpose_2d_array(rock_array)
    rock_array = tilt(rock_array)
    rock_array = transpose_2d_array(rock_array)
    return rock_array


def count_total_load_north_board(rock_array: list[list[str]]) -> int:
    length = len(rock_array)
    total = 0
    for i, row in enumerate(rock_array):
        total += (length - i) * row.count('O')
    return total


def count_total_load(rock_array: list[list[str]]) -> int:
    rock_array = tilt_north(rock_array)
    return count_total_load_north_board(rock_array)


def tilt_west(rock_array: list[list[str]]) -> list[list[str]]:
    rock_array = tilt(rock_array)
    return rock_array


def reverse_2d_array(rock_array: list[list[str]]) -> list[list[str]]:
    return [row[::-1] for row in rock_array]


def tilt_south(rock_array: list[list[str]]) -> list[list[str]]:
    rock_array = transpose_2d_array(rock_array)
    rock_array = reverse_2d_array(rock_array)
    rock_array = tilt(rock_array)
    rock_array = reverse_2d_array(rock_array)
    rock_array = transpose_2d_array(rock_array)
    return rock_array


def tilt_east(rock_array: list[list[str]]) -> list[list[str]]:
    rock_array = reverse_2d_array(rock_array)
    rock_array = tilt(rock_array)
    rock_array = reverse_2d_array(rock_array)
    return rock_array


def count_total_load_after_billion_cycles(rock_array: list[list[str]]) -> int:
    seen_states = {}
    i = 0
    billion = 1_000_000_000
    while i < billion:
        rock_array = tilt_north(rock_array)
        rock_array = tilt_west(rock_array)
        rock_array = tilt_south(rock_array)
        rock_array = tilt_east(rock_array)
        state_key = ''.join(''.join(row) for row in rock_array)

        if state_key in seen_states:
            loop_start = seen_states[state_key]
            loop_length = i - loop_start
            remainder = (billion - i) % loop_length
            i = billion - remainder
        else:
            seen_states[state_key] = i
        i += 1

    return count_total_load_north_board(rock_array)


def main() -> None:
    rock_array = files.read_file_into_2d_array('data.txt')
    rock_array = [list(row) for row in rock_array]
    total_load = count_total_load(rock_array)
    total_load_after_billion_cycles = count_total_load_after_billion_cycles(rock_array)

    print(f"1. The total load on the north support beams is equal to: {total_load}")
    print(f"2. The total load on the north support beams after one bilion cycles is equal to: {total_load_after_billion_cycles}")


if __name__ == "__main__":
    main()