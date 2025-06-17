import re

from utils import files


# Day 2: Cube Conundrum
# https://adventofcode.com/2023/day/2


def find_maxes(line: str) -> tuple[int, int, int]:
    red = find_max(r"\d+ red", line)
    green = find_max(r"\d+ green", line)
    blue = find_max(r"\d+ blue", line)
    return red, green, blue


def find_max(regex: str, line: str) -> int:
    return max((int(n) for n in re.findall(r"\d+", " ".join(re.findall(regex, line)))), default=0)


class Game:
    game_id: int
    possible: bool
    power: int

    def __init__(self, line: str) -> None:
        self.game_id = int(re.search(r"Game (\d+):", line).group(1))
        max_red, max_green, max_blue = find_maxes(line)
        self.possible = not (max_red > 12 or max_green > 13 or max_blue > 14)
        self.power = max_red * max_green * max_blue


def get_lists(lines: list[str]) -> tuple[list[int], list[int]]:
    games = [Game(line) for line in lines]
    ids = [game.game_id for game in games if game.possible]
    powers = [game.power for game in games]
    return ids, powers


def count_sums() -> tuple[int, int]:
    lines = files.read_file('data.txt')
    ids, powers = get_lists(lines)
    return sum(ids), sum(powers)


def main() -> None:
    ids_sum, powers_sum = count_sums()
    print(f"1. The sum of IDs of possible games is equal to {ids_sum}")
    print(f"2. The sum of powers of minimum sets is equal to {powers_sum}")


if __name__ == "__main__":
    main()
