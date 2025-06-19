from collections import Counter
from utils import files


# Day 7: Camel Cards
# https://adventofcode.com/2023/day/7


class Hand:
    cards: list[int]
    cards_joker_rule: list[int]
    bid: int
    hand_type: int
    hand_type_joker_rule: int

    CARD_MAP = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, 'T': 10,
        'J': 11, 'Q': 12, 'K': 13, 'A': 14
    }

    CARD_MAP_JOKER_RULE = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, 'T': 10,
        'J': 1, 'Q': 12, 'K': 13, 'A': 14
    }

    def __init__(self, line: str) -> None:
        parts = line.split()
        self.cards = [self.CARD_MAP[card] for card in parts[0]]
        self.cards_joker_rule = [self.CARD_MAP_JOKER_RULE[card] for card in parts[0]]
        self.bid = int(parts[1])
        self.hand_type = Hand.assign_type(self.cards)
        self.hand_type_joker_rule = Hand.assign_type_joker_rule(self.cards_joker_rule)

    @staticmethod
    def count_cards(cards: list[int], joker_rule: bool) -> Counter:
        counts = Counter(cards)
        if joker_rule:
            max_key = max(counts, key=counts.get)
            if max_key != 1:
                counts[max_key] += counts[1]
        return counts

    @staticmethod
    def choose_type(counts: Counter) -> int:
        if 5 in counts.values():
            return 7
        elif 4 in counts.values():
            return 6
        elif sorted(counts.values()) == [2, 3]:
            return 5
        elif 3 in counts.values():
            return 4
        elif list(counts.values()).count(2) == 2:
            return 3
        elif 2 in counts.values():
            return 2
        else:
            return 1

    @staticmethod
    def assign_type(cards: list[int]) -> int:
        counts = Hand.count_cards(cards, joker_rule=False)
        return Hand.choose_type(counts)

    @staticmethod
    def assign_type_joker_rule(cards: list[int]) -> int:
        num_jokers = cards.count(1)
        if num_jokers == 0:
            counts = Hand.count_cards(cards, joker_rule=False)
            return Hand.choose_type(counts)
        
        best_type = 0
        for replacement in range(2, 15):
            replaced = [card if card != 1 else replacement for card in cards]
            counts = Counter(replaced)
            hand_type = Hand.choose_type(counts)
            if hand_type > best_type:
                best_type = hand_type
        return best_type


def get_hands() -> list[Hand]:
    lines = files.read_file('data.txt')
    hands: list[Hand] = []
    for line in lines:
        hands.append(Hand(line))
    return hands


def sort_hands_by_type_and_cards(hands: list[Hand], use_joker_rule: bool = False) -> list[Hand]:
    if use_joker_rule:
        return sorted(hands, key=lambda hand: (hand.hand_type_joker_rule, hand.cards_joker_rule))
    else:
        return sorted(hands, key=lambda hand: (hand.hand_type, hand.cards))


def calculate_total_winnings(hands: list[Hand]) -> int:
    total = 0
    for rank, hand in enumerate(hands, 1):
        total += rank * hand.bid
    return total


def get_total_winnings() -> tuple[int, int]:
    hands = get_hands()
    all_hands_sorted = sort_hands_by_type_and_cards(hands)
    all_hands_sorted_joker_rule = sort_hands_by_type_and_cards(hands, use_joker_rule=True)
    total = calculate_total_winnings(all_hands_sorted)
    total_joker_rule = calculate_total_winnings(all_hands_sorted_joker_rule)
    return total, total_joker_rule


def main() -> None:
    total_winnings, total_winnings_joker_rule = get_total_winnings()
    print(f"1. The total winnings are equal to {total_winnings}")
    print(f"1. The total winnings using the joker rule are equal to {total_winnings_joker_rule}")


if __name__ == "__main__":
    main()