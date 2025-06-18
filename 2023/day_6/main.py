import math
import re
from utils import files
from utils import maths


# --- Day 6: Wait For It ---
# https://adventofcode.com/2023/day/6


def read_races_data(lines: list[str]) -> list[list[int]]:
    times = re.findall(r'\d+', lines[0].split(':')[1])
    distances = re.findall(r'\d+', lines[1].split(':')[1])
    return [[int(time), int(distance)] for time, distance in zip(times, distances)]


def count_ways_to_win(race: list[int]) -> int:
    time, distance = race
    solutions = maths.solve_quadratic_equation(-1, time, -distance)
    solutions = sorted(solutions)

    if len(solutions) < 2:
        return 0

    start_bound = math.ceil(solutions[0])
    if start_bound == solutions[0]:
        start_bound += 1

    end_bound = math.floor(solutions[1])
    if end_bound == solutions[1]:
        end_bound -= 1

    return end_bound + 1 - start_bound


def product_of_ways_to_win(lines: list[str]) -> int:
    races = read_races_data(lines)
    return math.prod([count_ways_to_win(race) for race in races])


def read_race_data(lines: list[str]) -> list[int]:
    times = re.findall(r'\d+', lines[0].split(':')[1])
    distances = re.findall(r'\d+', lines[1].split(':')[1])
    time = "".join(times)
    distance = "".join(distances)
    return [int(time), int(distance)]


def ways_to_win_longer_race(lines: list[str]) -> int:
    return count_ways_to_win(read_race_data(lines))


def main() -> None:
    lines = files.read_file('data.txt')
    print(f"1. The product of numbers of ways you can win the races is equal to {product_of_ways_to_win(lines)}")
    print(f"2. The ways you can win one longer race is equal to {ways_to_win_longer_race(lines)}")


if __name__ == "__main__":
    main()