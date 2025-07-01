from dataclasses import dataclass
import re
from utils import files


# Day 15: Lens Library
# https://adventofcode.com/2023/day/15


@dataclass
class Box:
    lenses: list[tuple[str, int]]
    
    def operation(self, label: str, symbol: str, focal_length: int | None = None) -> None:
        if symbol == '-':
            self.dash_operation(label)
        else:
            self.equal_operation(label, focal_length)

    def dash_operation(self, label: str) -> None:
        self.lenses = [lens for lens in self.lenses if lens[0] != label]

    def equal_operation(self, label: str, focal_length: int) -> None:
        for i, lens in enumerate(self.lenses):
            if label == lens[0]:
                self.lenses[i] = (label, focal_length)
                return
        self.lenses.append((label, focal_length))

    def count_focus_power(self, number: int) -> int:
        return sum((number + 1) * (i + 1) * lens[1] for i, lens in enumerate(self.lenses))


def get_steps() -> list[str]:
    line = files.read_file('data.txt')
    return line[0].split(',')


def count_hash(step: str) -> int:
    value = 0
    for char in step:
        value += ord(char)
        value *= 17
        value %= 256

    return value


def count_sum_hashes(steps: list[str]) -> int:
    hashes = [count_hash(step) for step in steps]
    return sum(hashes)


def parse_steps(steps: list[str]) -> list[list[str]]:
    pattern = r'[a-z]+|[-=]|[1-9]'
    return [re.findall(pattern, step) for step in steps]


def count_sum_focusing_power(steps: list[str]) -> int:
    boxes = {i: Box([]) for i in range(256)}
    parsed_steps = parse_steps(steps)
    for step in parsed_steps:
        hash_value = count_hash(step[0])
        if len(step) == 2:
            boxes[hash_value].operation(step[0], step[1])
        else:
            boxes[hash_value].operation(step[0], step[1], int(step[2]))
    
    focus_powers = [box.count_focus_power(number) for number, box in boxes.items()]
    return sum(focus_powers)


def main() -> None:
    steps = get_steps()
    sum_hashes = count_sum_hashes(steps)
    sum_focusing_power = count_sum_focusing_power(steps)
    
    print(f"1. The sum of all hashes is equal to: {sum_hashes}")
    print(f"2. The sum of focusing power is equal to: {sum_focusing_power}")


if __name__ == "__main__":
    main()