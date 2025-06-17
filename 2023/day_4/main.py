import re
from typing import List, Optional
from utils import files


# Day 4: Scratchcards
# https://adventofcode.com/2023/day/4


def parse_lines(lines: list[str]) -> list[list[list[str]]]:
    result: list[list[list[str]]] = []

    for line in lines:
        parts = line.split(':')[1].split('|')
        winning_numbers = re.findall(r'\d+', parts[0])
        my_numbers = re.findall(r'\d+', parts[1])
        result.append([winning_numbers, my_numbers])

    return result


def get_cards() -> list[list[list[str]]]:
    lines = files.read_file('data.txt')
    return parse_lines(lines)


def count_power(card: list[list[str]]) -> Optional[int]:
    matches = sum(1 for my in card[1] for win in card[0] if my == win)
    return matches - 1 if matches > 0 else None


def count_points(cards: list[list[list[str]]]) -> int:
    points = 0
    for card in cards:
        power = count_power(card)
        if power is not None:
            points += 2 ** power
    return points


def count_occurrences(card: list[list[str]]) -> int:
    return sum(1 for my in card[1] for win in card[0] if my == win)


def count_cards(cards: list[list[list[str]]]) -> int:
    counts = [1] * len(cards)

    for i, card in enumerate(cards):
        occurrences = count_occurrences(card)
        for _ in range(counts[i]):
            for j in range(i + 1, min(i + occurrences + 1, len(cards))):
                counts[j] += 1

    return sum(counts)


def main() -> None:
    cards = get_cards()
    sum_of_points = count_points(cards)
    sum_of_cards = count_cards(cards)
    print(f"1. The sum of points is equal to {sum_of_points}")
    print(f"2. The sum of cards is equal to {sum_of_cards}")


if __name__ == "__main__":
    main()