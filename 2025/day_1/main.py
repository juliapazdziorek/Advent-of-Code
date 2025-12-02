from utils import files

# Day 1: Secret Entrance
# https://adventofcode.com/2025/day/1


def parse_instructions(lines: list[str]) -> list[int]:
    return [(-1 if line[0] == 'L' else 1) * int(line[1:]) for line in lines]


def count_zeros(instructions: list[int]) -> int:
    current_point = 50
    counter = 0

    for instruction in instructions:
        current_point += instruction
        if current_point > 99 or current_point < 0:
            current_point %= 100
        if current_point == 0:
            counter += 1
            
    return counter


def count_zeros_during_rotations(instructions: list[int]) -> int:
    current_point = 50
    counter = 0

    for instruction in instructions:
        if current_point == 0 and instruction < 0:
            counter -= 1

        current_point += instruction

        if current_point > 99:
            rotations = current_point // 100
            if current_point % 100 == 0:
                rotations -= 1
            counter += rotations
            
        elif current_point < 0:
            rotations = (abs(current_point) // 100) + 1
            if current_point % 100 == 0:
                rotations -= 1
            counter += rotations

        current_point %= 100

        if current_point == 0:
            counter += 1

    return counter


def main() -> None:
    lines = files.read_file('data.txt')
    instructions = parse_instructions(lines)
    zeros = count_zeros(instructions)
    zeros_during_rotations = count_zeros_during_rotations(instructions)

    print(f"1. The numer of zeros hit at the end of each instruction is equal to {zeros}")
    print(f"2. The numer of zeros hit at the during every instruction is equal to {zeros_during_rotations}")


if __name__ == "__main__":
    main()