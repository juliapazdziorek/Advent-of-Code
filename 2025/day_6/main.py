from utils import files
from dataclasses import dataclass

# Day 6: Trash Compactor
# https://adventofcode.com/2025/day/6


@dataclass
class Problem:
    numbers: list[int]
    operation: str


    def solve(self) -> int:
        if self.operation == "+":
            result = sum(self.numbers)
        else:
            result = 1
            for number in self.numbers:
                result *= number
        return result


def parse_problems(lines: list[str]) -> list[Problem]:
    number_lines = [[int(number) for number in line.split()] for line in lines[:-1]]
    operations = lines[-1].split()
    return [Problem([number_line[i] for number_line in number_lines], operations[i]) for i in range(len(number_lines[0]))]


def count_sum_answers(problems: list[Problem]) -> int:
    return sum([problem.solve() for problem in problems])


def correctly_parse_problems(lines: list[str]) -> list[Problem]:
    number_lines = [[char for char in line] for line in lines[:-1]]
    numbers = []
    current_numbers = []
    for i in range(len(number_lines[0])):
        number_chars = [number_line[i] for number_line in number_lines]
        number = ''.join(number_chars).strip()
        if number:
            current_numbers.append(int(number))
        else:
            numbers.append(current_numbers)
            current_numbers = []
    numbers.append(current_numbers)

    operations = lines[-1].split()
    return [Problem(numbers[i], operations[i]) for i in range(len(numbers))]


def main() -> None:
    lines = files.read_file('data.txt')
    problems = parse_problems(lines)
    sum_answers = count_sum_answers(problems)
    correctly_read_problems = correctly_parse_problems(lines)
    correct_sum_answers = count_sum_answers(correctly_read_problems)

    print(f"1. The grand total of answers is equal to: {sum_answers}")
    print(f"2. The grand total of answers of correctly read problems is equal to: {correct_sum_answers}")


if __name__ == "__main__":
    main()