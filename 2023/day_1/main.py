from typing import Optional

from utils import files


# Day 1: Trebuchet Calibration
# https://adventofcode.com/2023/day/1


digit_dict = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"
}


def lines_to_digits(line: str) -> str:
    result = []
    i = 0
    while i < len(line):
        if line[i].isdigit():
            result.append(line[i])
        else:
            for word, digit in digit_dict.items():
                if line.startswith(word, i):
                    result.append(digit)
                    break
        i += 1
    return ''.join(result)


def get_digit(line: str, reverse: bool = False) -> Optional[str]:
    iterable = reversed(line) if reverse else line
    for char in iterable:
        if char.isdigit():
            return char
    return None


def get_calibration_values(lines: list[str], to_digits: bool) -> list[int]:
    values = []
    for line in lines:
        processed_line = lines_to_digits(line) if to_digits else line
        first = get_digit(processed_line)
        last = get_digit(processed_line, reverse=True)
        if first and last:
            values.append(int(first + last))
    return values


def count_sum_calibration_values(lines: list[str], to_digits: bool) -> int:
    return sum(get_calibration_values(lines, to_digits))


def main() -> None:
    lines = files.read_file('data.txt')
    print(f"1. The sum of calibration values is equal to {count_sum_calibration_values(lines, False)}")
    print(f"2. The sum of calibration values considering digits written as words is equal to {count_sum_calibration_values(lines, True)}")


if __name__ == "__main__":
    main()
